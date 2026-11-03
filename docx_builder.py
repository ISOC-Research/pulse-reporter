"""
docx_builder.py
===============
Turns the HTML fragment produced by the LLM policy-brief generators into a
Word report that looks like ISOC_Sample.docx.

It opens templates/ISOC_Template.docx (cover page, header/footer, styles and
theme cloned from the official sample) and appends the report body using the
sample's own styles (Heading 1-4, List Paragraph, Caption, navy #0F2A47 tables).

Public API:
    build_docx(llm_html, topic_title, country_code, out_path)
"""
import os
import re
from datetime import datetime

import docx
from bs4 import BeautifulSoup, NavigableString, Tag
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from docx_charts import parse_chart_json, render_chart, render_mermaid
from isoc_theme import NAVY_TABLE, BODY_TEXT, TABLE_FONT

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "templates", "ISOC_Template.docx")

COUNTRY_NAMES = {
    "SO": "Somalia", "IN": "India", "FR": "France", "MA": "Morocco", "KE": "Kenya",
    "NG": "Nigeria", "ZA": "South Africa", "EG": "Egypt", "US": "United States",
    "GB": "United Kingdom", "DE": "Germany", "BR": "Brazil", "ET": "Ethiopia",
    "GH": "Ghana", "TZ": "Tanzania", "UG": "Uganda", "SN": "Senegal", "CI": "Côte d'Ivoire",
}

_EMOJI_RE = re.compile(
    "[\U00010000-\U0010FFFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u2300-\u23FF]+"
)


def country_name(code):
    code = code.upper()
    if code in COUNTRY_NAMES:
        return COUNTRY_NAMES[code]
    try:
        import pycountry
        c = pycountry.countries.get(alpha_2=code)
        if c:
            return getattr(c, "common_name", c.name)
    except Exception:
        pass
    return code


def clean(text):
    """Remove emoji (the brand font has no glyphs for them) and tidy spaces."""
    text = _EMOJI_RE.sub("", text or "")
    return re.sub(r"[ \t]+", " ", text).strip()


# ───────────────────────────── low-level helpers ─────────────────────────────

def _shade(cell, hex_fill):
    tcpr = cell._tc.get_or_add_tcPr()
    for old in tcpr.findall(qn("w:shd")):
        tcpr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcpr.append(shd)


def _cell_borders(cell, **edges):
    """edges: top/bottom/left/right = (size, hex_color) or None for nil."""
    tcpr = cell._tc.get_or_add_tcPr()
    borders = tcpr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcpr.append(borders)
    for edge, spec in edges.items():
        el = OxmlElement(f"w:{edge}")
        if spec is None:
            el.set(qn("w:val"), "nil")
        else:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(spec[0]))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), spec[1])
        borders.append(el)


def _cell_margins(cell, top=70, bottom=70, left=110, right=110):
    tcpr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{k}")
        e.set(qn("w:w"), str(v))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tcpr.append(mar)


def _run_font(run, size=None, bold=None, italic=None, color=None, name=None):
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    if name:
        run.font.name = name
        run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_inline(par, node, size=None, color=None, font=None, bold=False, italic=False):
    """Append inline HTML (strong/em/br/a/span...) to a paragraph."""
    for child in node.children:
        if isinstance(child, NavigableString):
            text = re.sub(r"\s+", " ", _EMOJI_RE.sub("", str(child)))
            if not par.text or par.text.endswith((" ", "\u00A0", "\n")):
                text = text.lstrip()
            if not text:
                continue
            r = par.add_run(text)
            _run_font(r, size=size, bold=bold, italic=italic, color=color, name=font)
        elif isinstance(child, Tag):
            if child.name == "br":
                par.add_run().add_break()
            elif child.name in ("strong", "b"):
                add_inline(par, child, size, color, font, True, italic)
            elif child.name in ("em", "i"):
                add_inline(par, child, size, color, font, bold, True)
            elif child.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                if par.text.strip():
                    par.add_run().add_break()
                add_inline(par, child, size, color, font, True, italic)
                par.add_run().add_break()
            elif child.name in ("p", "div"):
                if par.text.strip() and not par.text.endswith("\n"):
                    par.add_run().add_break()
                add_inline(par, child, size, color, font, bold, italic)
            else:
                add_inline(par, child, size, color, font, bold, italic)


# ───────────────────────────── block builders ─────────────────────────────

_TABLE_PRESETS = {
    # first-header(s) key -> column widths in inches (total 6.66)
    ("indicator", 4, "benchmark"): [2.0, 1.25, 1.25, 2.16],      # Key numbers at a glance
    ("action", 4, "owner"): [1.45, 2.55, 1.05, 1.61],             # 4.1 / 4.2
    ("action", 3, "outcome"): [1.6, 3.1, 1.96],                   # 4.3
    ("#", 5, "quick win"): [0.35, 1.45, 2.25, 0.8, 1.81],         # 5. Quick wins
    ("gap", 3, "consequence"): [1.8, 2.4, 2.46],                  # 6.1
    ("indicator", 4, "baseline"): [2.2, 1.2, 1.4, 1.86],          # 7. Measuring progress
    ("ixp", 5, "ipv6"): [1.9, 1.0, 1.1, 1.4, 1.26],               # IXP table
    ("asn", 5, "isp"): [0.95, 2.25, 1.1, 1.1, 1.26],              # 5-col operator table
    ("asn", 6, "isp"): [0.85, 1.95, 0.9, 0.9, 1.1, 0.96],         # 6-col operator table
    ("asn", 7, "isp"): [0.8, 1.65, 0.8, 0.8, 0.8, 1.0, 0.81],     # 7-col operator table
    ("asn", 8, "isp"): [0.74, 1.46, 0.66, 0.68, 0.56, 0.72, 1.04, 0.80],  # 8-col operator table
}


def _preset_widths(head_cells, ncols):
    """Pick column widths matching the sample's tables; None -> equal widths."""
    if not head_cells:
        return None
    heads = [clean(c.get_text(" ")).lower() for c in head_cells]
    if len(heads) < 2:
        return None
    for (first, n, second), widths in _TABLE_PRESETS.items():
        if n == ncols and heads[0].startswith(first) and (
                heads[1].startswith(second) or (n == 4 and second in heads) or second in heads):
            return widths
    return None


class Builder:
    def __init__(self, document):
        self.doc = document
        self.fig_no = 0
        self.first_h1 = True

    # headings -------------------------------------------------------------
    def heading(self, text, level):
        text = clean(text)
        if not text:
            return
        p = self.doc.add_paragraph(text, style=f"Heading {min(level, 4)}")
        if level == 1:
            # every major section starts on a new page, like the sample
            p.paragraph_format.page_break_before = True
        p.paragraph_format.keep_with_next = True

    # paragraphs / lists ---------------------------------------------------
    def paragraph(self, tag):
        p = self.doc.add_paragraph(style="Normal")
        add_inline(p, tag)
        if not p.text.strip():
            p._element.getparent().remove(p._element)

    def list_block(self, tag, ordered=False):
        n = 0
        for li in tag.find_all("li", recursive=False):
            n += 1
            if ordered:
                # numbered: Normal paragraph with hanging indent + manual number
                p = self.doc.add_paragraph(style="Normal")
                pf = p.paragraph_format
                pf.left_indent = Inches(0.32)
                pf.first_line_indent = Inches(-0.32)
                pf.tab_stops.add_tab_stop(Inches(0.32))
                pf.space_after = Pt(3)
                r = p.add_run(f"{n}.\t")
                r.bold = True
            else:
                # bullets come from the sample's List Paragraph style itself
                p = self.doc.add_paragraph(style="List Paragraph")
                p.paragraph_format.space_after = Pt(3)
            # inline content only (skip nested lists, handle after)
            inline = BeautifulSoup("", "html.parser")
            holder = inline.new_tag("span")
            nested = []
            for c in li.children:
                if isinstance(c, Tag) and c.name in ("ul", "ol"):
                    nested.append(c)
                else:
                    holder.append(c.__copy__() if hasattr(c, "__copy__") else c)
            add_inline(p, holder)
            for nl in nested:
                self.list_block(nl, ordered=(nl.name == "ol"))
        self.doc.add_paragraph(style="Normal").paragraph_format.space_after = Pt(2)

    # tables ---------------------------------------------------------------
    def table(self, tag):
        rows = []
        head_cells = None
        thead = tag.find("thead")
        if thead:
            tr = thead.find("tr")
            if tr:
                head_cells = tr.find_all(["th", "td"])
        body_trs = tag.find("tbody").find_all("tr") if tag.find("tbody") else [
            tr for tr in tag.find_all("tr") if not (thead and tr in thead.find_all("tr"))]
        for tr in body_trs:
            cells = tr.find_all(["td", "th"])
            if head_cells is None and tr.find("th") and not rows:
                head_cells = cells
                continue
            rows.append(cells)
        ncols = max([len(head_cells or [])] + [len(r) for r in rows] or [0])
        if ncols == 0:
            return
        self._navy_table(head_cells, rows, ncols, widths=_preset_widths(head_cells, ncols))

    def chart(self, raw_json):
        """Structured chart block (donut/bar/line/matrix) rendered with matplotlib."""
        try:
            spec = parse_chart_json(raw_json)
        except Exception as exc:
            print(f"   [warn] Chart JSON invalid ({exc})".encode("ascii", "replace").decode())
            return
        img = render_chart(spec)
        if not img:
            return
        self.fig_no += 1
        p = self.doc.add_paragraph(style="Normal")
        p.alignment = 1
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(img, width=Inches(5.7 if spec.get("type") != "matrix" else 5.4))
        cap = self.doc.add_paragraph(style="Caption body copy")
        r = cap.add_run(f"Figure {self.fig_no}. ")
        r.bold = True
        cap.add_run(clean(spec.get("caption") or spec.get("title") or "Chart"))
        try:
            os.remove(img)
        except OSError:
            pass

    def _navy_table(self, head_cells, rows, ncols, widths=None):
        t = self.doc.add_table(rows=0, cols=ncols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        total = 6.66
        widths = widths or [total / ncols] * ncols

        def fill_row(cells, header):
            row = t.add_row()
            if header:
                trpr = row._tr.get_or_add_trPr()
                th = OxmlElement("w:tblHeader")
                trpr.append(th)
            cant = OxmlElement("w:cantSplit")
            row._tr.get_or_add_trPr().append(cant)
            for i in range(ncols):
                cell = row.cells[i]
                cell.width = Inches(widths[i])
                _cell_margins(cell)
                src = cells[i] if i < len(cells) else None
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(0)
                par.paragraph_format.space_before = Pt(0)
                if src is not None:
                    if header:
                        add_inline(par, src, size=9.5, color="FFFFFF", font=TABLE_FONT, bold=True)
                    else:
                        add_inline(par, src, size=9.5, color=BODY_TEXT, font=TABLE_FONT)
                if header:
                    _shade(cell, NAVY_TABLE)
                    _cell_borders(cell, top=None, left=None, right=None, bottom=None)
                else:
                    _shade(cell, "FFFFFF")
                    _cell_borders(cell, top=None, left=None, right=None, bottom=(4, "C9D3DF"))

        if head_cells:
            fill_row(head_cells, True)
        for r in rows:
            fill_row(r, False)
        self.doc.add_paragraph(style="Normal").paragraph_format.space_after = Pt(4)

    # stat cards -> "Key numbers at a glance" table --------------------------
    def stat_grid(self, tag):
        rows = []
        for card in tag.select(".stat-card"):
            num = card.select_one(".number")
            lab = card.select_one(".label")
            rows.append((clean(lab.get_text(" ")) if lab else "", clean(num.get_text(" ")) if num else ""))
        if not rows:
            return
        soup = BeautifulSoup("", "html.parser")

        def cell(txt):
            s = soup.new_tag("span")
            s.string = txt
            return s

        self._navy_table([cell("Key number"), cell("Value")],
                         [[cell(a), cell(b)] for a, b in rows], 2, widths=[4.66, 2.0])

    # callouts ---------------------------------------------------------------
    def callout(self, tag, kind=""):
        colors = {"": ("EAF1FB", "3A82E4"), "callout-warning": ("FDF1E3", "D25238"),
                  "callout-success": ("E6F5F2", "40B2A4")}
        fill, bar = colors.get(kind, colors[""])
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t.rows[0].cells[0]
        cell.width = Inches(6.66)
        _shade(cell, fill)
        _cell_margins(cell, 110, 110, 180, 140)
        _cell_borders(cell, left=(36, bar), top=None, bottom=None, right=None)
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        add_inline(par, tag, size=10.5, color=BODY_TEXT)
        self.doc.add_paragraph(style="Normal").paragraph_format.space_after = Pt(4)

    # figures ------------------------------------------------------------------
    def figure(self, title, mermaid_text):
        img = render_mermaid(mermaid_text, title)
        if not img:
            return
        self.fig_no += 1
        p = self.doc.add_paragraph(style="Normal")
        p.alignment = 1
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(img, width=Inches(5.4))
        cap = self.doc.add_paragraph(style="Caption body copy")
        r = cap.add_run(f"Figure {self.fig_no}. ")
        r.bold = True
        cap.add_run(clean(title) or "Chart")
        try:
            os.remove(img)
        except OSError:
            pass

    # phases / swot / verdict ------------------------------------------------
    def phase(self, tag):
        badge = tag.select_one(".phase-badge")
        if badge:
            self.heading(badge.get_text(" "), 3)
        for child in tag.children:
            if isinstance(child, Tag) and child.name in ("ul", "ol"):
                self.list_block(child, ordered=(child.name == "ol"))
            elif isinstance(child, Tag) and child.name == "p":
                self.paragraph(child)

    def swot(self, tag):
        for card in tag.select(".swot-card"):
            h = card.find(["h3", "h2"])
            if h:
                self.heading(h.get_text(" "), 3)
            for lst in card.find_all(["ul", "ol"], recursive=False):
                self.list_block(lst, ordered=(lst.name == "ol"))

    def verdict(self, tag):
        h = tag.find(["h2", "h1"])
        if h:
            self.heading(h.get_text(" "), 2)
        scores = []
        for item in tag.select(".verdict-item"):
            s = item.select_one(".score")
            l = item.select_one(".score-label")
            scores.append((clean(l.get_text(" ")) if l else "", clean(s.get_text(" ")) if s else ""))
        for c in tag.children:
            if isinstance(c, Tag) and c.name in ("p",):
                self.paragraph(c)
            elif isinstance(c, Tag) and c.name in ("ul", "ol"):
                self.list_block(c, ordered=(c.name == "ol"))
        if scores:
            soup = BeautifulSoup("", "html.parser")

            def cell(txt):
                s = soup.new_tag("span")
                s.string = txt
                return s
            self._navy_table([cell("Indicator"), cell("Assessment")],
                             [[cell(a), cell(b)] for a, b in scores], 2, widths=[4.0, 2.66])

    # dispatcher -------------------------------------------------------------
    def walk(self, node):
        for child in node.children:
            if isinstance(child, NavigableString):
                continue
            name = child.name
            classes = child.get("class") or []
            if name == "h1":
                self.heading(child.get_text(" "), 1)
            elif name == "h2":
                self.heading(child.get_text(" "), 2)
            elif name in ("h3", "h4"):
                self.heading(child.get_text(" "), 3 if name == "h3" else 4)
            elif name == "p":
                self.paragraph(child)
            elif name in ("ul", "ol"):
                self.list_block(child, ordered=(name == "ol"))
            elif name == "table":
                self.table(child)
            elif name == "pre":
                p = self.doc.add_paragraph(child.get_text(), style="Normal")
            elif name == "div":
                if "stat-grid" in classes:
                    self.stat_grid(child)
                elif "swot-grid" in classes:
                    self.swot(child)
                elif "callout" in classes:
                    kind = next((c for c in classes if c.startswith("callout-")), "")
                    self.callout(child, kind)
                elif "phase" in classes:
                    self.phase(child)
                elif "verdict" in classes:
                    self.verdict(child)
                elif "isoc-chart" in classes:
                    self.chart(child.get_text())
                elif "chart-container" in classes:
                    h = child.find("h3")
                    m = child.select_one(".mermaid")
                    if m:
                        self.figure(h.get_text(" ") if h else "", m.get_text())
                elif "mermaid" in classes:
                    self.figure("", child.get_text())
                elif "footer" in classes:
                    continue
                else:
                    self.walk(child)
            else:
                self.walk(child)


# ───────────────────────────── public API ─────────────────────────────

def _fill_placeholders(root, mapping):
    for t in root.iter(qn("w:t")):
        if t.text and "{" in t.text:
            for k, v in mapping.items():
                t.text = t.text.replace(k, v)


def _refresh_toc_silent(docx_path):
    """Pre-populate the Table of Contents via headless Word (if available) and clear dirty flags
    so Microsoft Word never shows the 'update fields that may refer to other files' dialog on open."""
    abs_path = os.path.abspath(docx_path)
    if os.name == "nt":
        import subprocess
        ps = (
            "$ErrorActionPreference='Stop';"
            "$w=New-Object -ComObject Word.Application;$w.Visible=$false;$w.DisplayAlerts=0;"
            f"$d=$w.Documents.Open('{abs_path}');"
            "foreach($t in $d.TablesOfContents){$t.Update()};"
            "$d.Save();$d.Close(0);$w.Quit()"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        except Exception:
            pass
    try:
        d = docx.Document(abs_path)
        for fc in d.element.iter(qn("w:fldChar")):
            if qn("w:dirty") in fc.attrib:
                del fc.attrib[qn("w:dirty")]
        settings = d.settings.element
        for uf in settings.findall(qn("w:updateFields")):
            settings.remove(uf)
        d.save(abs_path)
    except Exception:
        pass


def build_docx(llm_html, topic_title, country_code, out_path):
    if not os.path.exists(TEMPLATE):
        raise FileNotFoundError(
            f"{TEMPLATE} not found - run `python build_template.py` first.")
    document = docx.Document(TEMPLATE)
    mapping = {
        "{COUNTRY}": country_name(country_code),
        "{TOPIC}": topic_title,
        "{DATE}": datetime.now().strftime("%B %Y"),
    }
    _fill_placeholders(document.element.body, mapping)
    for sec in document.sections:
        for part in (sec.header, sec.first_page_header, sec.even_page_header,
                     sec.footer, sec.first_page_footer, sec.even_page_footer):
            _fill_placeholders(part._element, mapping)

    soup = BeautifulSoup(llm_html, "html.parser")
    Builder(document).walk(soup)

    core = document.core_properties
    core.title = f"Internet Resilience in {mapping['{COUNTRY}']} – {topic_title} report"
    core.author = "ISOC Pulse"
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    document.save(out_path)
    _refresh_toc_silent(out_path)
    return out_path


def export_word_safe(llm_html, topic_title, country_code, out_path):
    """Used by the brief generators: never let a Word-export problem break the HTML flow."""
    try:
        build_docx(llm_html, topic_title, country_code, out_path)
        print(f"Success! Word report saved to: {out_path}")
        return out_path
    except Exception as exc:  # pragma: no cover
        print(f"[warn] Word export failed ({exc}); HTML brief is unaffected.")
        return None
