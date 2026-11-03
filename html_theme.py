"""
html_theme.py
=============
Re-skins the HTML policy-brief templates (generate_llm_brief.py /
generate_dnssec_brief.py) with the ISOC look taken from ISOC_Sample.docx and
adds the "Download Word report" button.

The data/LLM pipeline is untouched: we only swap the <style> block, the cover
block, the font link and (optionally) the Mermaid palette inside the template
string *before* it is `.format()`-ed by the generators.

Usage inside a generator:
    html_template = apply_isoc_theme(HTML_TEMPLATE, topic_title, docx_filename,
                                     country_code, semantic_pies=False)
"""
import base64
import io
import os
import re
import zipfile
from functools import lru_cache

from isoc_theme import (BRIGHT_BLUE, CORAL, DARK_NAVY, DEEP_INDIGO, GOLD,
                        NAVY_TABLE, OFF_WHITE, PLUM, TEAL)

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DOCX = os.path.join(HERE, "templates", "ISOC_Template.docx")

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700'
             '&display=swap" rel="stylesheet">')

CSS = """
:root {
    --navy: #0C1C2C;
    --table-navy: #0F2A47;
    --blue: #3A82E4;
    --indigo: #24366E;
    --h3: #121A36;
    --h4: #1B2852;
    --teal: #40B2A4;
    --plum: #7E245C;
    --coral: #D25238;
    --gold: #EECA4A;
    --offwhite: #EEF2EC;
    --grey: #DEDAD0;
    --rule: #C9D3DF;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Hind', 'Segoe UI', Arial, sans-serif;
    font-weight: 300;
    font-size: 16px;
    line-height: 1.65;
    color: var(--navy);
    background: #ffffff;
}
strong { font-weight: 600; color: var(--table-navy); }

/* ── DOWNLOAD BUTTON ── */
.download-bar {
    position: fixed; top: 16px; right: 16px; z-index: 50;
}
.download-btn {
    display: inline-flex; align-items: center; gap: 10px;
    background: var(--blue); color: #fff !important; text-decoration: none;
    font-family: 'Hind', Arial, sans-serif; font-weight: 600; font-size: 14px;
    padding: 11px 20px; border-radius: 4px;
    box-shadow: 0 4px 14px rgba(12,28,44,0.35);
    transition: background .15s ease, transform .15s ease;
}
.download-btn:hover { background: var(--indigo); transform: translateY(-1px); }
.download-btn svg { width: 18px; height: 18px; fill: currentColor; }
.download-btn.large { font-size: 16px; padding: 14px 28px; margin-top: 8px; }

/* ── COVER (mirrors the Word cover page) ── */
.cover {
    min-height: 100vh;
    background: #0C1C2C url('@@COVER_IMG@@') center top / cover no-repeat;
    color: var(--offwhite);
    display: flex; flex-direction: column; justify-content: center;
    padding: 80px 8vw 70px;
    position: relative;
    page-break-after: always;
}
.cover-draft {
    position: absolute; top: 40px; left: 8vw;
    font-size: 13px; font-weight: 600; letter-spacing: 1px; text-decoration: underline;
    color: #fff;
}
.cover-date { font-size: 16px; margin-bottom: 44px; opacity: .9; }
.cover-country {
    font-size: clamp(34px, 5.2vw, 56px); font-weight: 300; line-height: 1.12;
    color: var(--offwhite); max-width: 760px; margin-bottom: 22px;
}
.cover-title { font-size: 22px; font-weight: 300; margin-bottom: 44px; opacity: .95; }
.cover-line { display: none; }
.cover-meta { font-size: 15px; line-height: 1.9; opacity: .85; }
.cover-brand {
    position: absolute; right: 8vw; bottom: 46px;
    font-size: 26px; font-weight: 600; letter-spacing: .5px; line-height: 1.1; text-align: left;
}

/* ── BODY ── */
.content { max-width: 860px; margin: 0 auto; padding: 56px 36px 40px; }

h1 {
    font-size: 30px; font-weight: 400; color: var(--blue);
    margin: 64px 0 22px; padding-bottom: 8px; border-bottom: 1px solid var(--rule);
    page-break-before: always;
}
h1:first-child { margin-top: 0; page-break-before: avoid; }
h2 { font-size: 22px; font-weight: 500; color: var(--indigo); margin: 36px 0 12px; }
h3 { font-size: 18px; font-weight: 500; color: var(--h3); margin: 26px 0 10px; }
h4 { font-size: 16px; font-weight: 600; color: var(--h4); margin: 20px 0 8px; }
p { margin-bottom: 14px; }
ul, ol { padding-left: 26px; margin-bottom: 14px; }
li { margin-bottom: 7px; }
li::marker { color: var(--blue); }

/* ── KEY NUMBERS ── */
.stat-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px; margin: 24px 0;
}
.stat-card {
    background: #fff; padding: 18px 20px; text-align: left;
    border: 1px solid var(--rule); border-top: 4px solid var(--blue);
}
.stat-card .number { font-size: 34px; font-weight: 600; color: var(--table-navy); display: block; line-height: 1.15; }
.stat-card .label {
    font-family: Arial, sans-serif; font-size: 12px; font-weight: 400; color: #4a5a6a;
    text-transform: uppercase; letter-spacing: .6px; margin-top: 6px; display: block;
}

/* ── TABLES (navy header, like the report) ── */
table {
    width: 100%; border-collapse: collapse; margin: 22px 0;
    font-family: Arial, sans-serif; font-size: 13.5px; color: #22303C;
}
thead th {
    background: var(--table-navy); color: #fff; font-weight: 700; text-align: left;
    padding: 11px 14px; font-size: 13px;
}
tbody td { padding: 10px 14px; border-bottom: 1px solid var(--rule); background: #fff; }
tbody tr:hover td { background: #F3F7FC; }

/* ── SWOT ── */
.swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 24px 0; }
.swot-card { padding: 20px 22px; border-left: 5px solid var(--blue); background: #EAF1FB; }
.swot-card h3 { margin: 0 0 10px; font-size: 17px; font-weight: 600; }
.swot-card ul { padding-left: 20px; margin: 0; }
.swot-card li { font-size: 14.5px; margin-bottom: 8px; }
.swot-strengths     { background: #E6F5F2; border-left-color: var(--teal); }
.swot-strengths h3  { color: #26867A; }
.swot-weaknesses    { background: #FBEAE6; border-left-color: var(--coral); }
.swot-weaknesses h3 { color: var(--coral); }
.swot-opportunities { background: #EAF1FB; border-left-color: var(--blue); }
.swot-opportunities h3 { color: var(--indigo); }
.swot-threats       { background: #FDF6DC; border-left-color: var(--gold); }
.swot-threats h3    { color: #8A6D0B; }

/* ── CALLOUTS ── */
.callout {
    background: #EAF1FB; border-left: 5px solid var(--blue);
    padding: 16px 22px; margin: 22px 0; font-size: 15px;
}
.callout-warning { background: #FBEAE6; border-left-color: var(--coral); }
.callout-success { background: #E6F5F2; border-left-color: var(--teal); }

/* ── VERDICT ── */
.verdict { background: var(--table-navy); color: #fff; padding: 36px 40px; margin: 44px 0; }
.verdict h2 { color: #fff; margin: 0 0 16px; font-size: 24px; border: none; }
.verdict p, .verdict li { color: rgba(255,255,255,.92); }
.verdict strong { color: #fff; }
.verdict-scores { display: flex; gap: 56px; margin-top: 22px; flex-wrap: wrap; }
.verdict-item .score { font-size: 28px; font-weight: 600; color: var(--gold); }
.verdict-item .score-label {
    font-family: Arial, sans-serif; font-size: 12px; text-transform: uppercase;
    letter-spacing: .6px; opacity: .75; margin-top: 4px;
}

/* ── CHARTS ── */
.chart-container {
    background: #fff; padding: 22px 26px; margin: 26px 0; border: 1px solid var(--rule); text-align: center;
}
.chart-container h3 { margin: 0 0 16px; text-align: left; font-size: 16px; color: var(--indigo); }
.mermaid { margin: 0 auto; }

/* ── ROADMAP PHASES ── */
.phase { background: #fff; padding: 22px 26px; margin: 16px 0; border: 1px solid var(--rule); border-left: 5px solid var(--blue); }
.phase-badge {
    display: inline-block; background: var(--blue); color: #fff;
    font-family: Arial, sans-serif; font-size: 12px; font-weight: 700;
    padding: 4px 14px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: .8px;
}
.phase-badge.medium { background: var(--indigo); }
.phase-badge.long { background: var(--table-navy); }
.phase ol, .phase ul { margin-bottom: 0; }
.phase li { font-size: 15px; }

/* ── FOOTER ── */
.footer {
    text-align: left; padding: 30px 0 0; margin-top: 60px;
    border-top: 1px solid var(--rule); color: #5b6b7b; font-size: 13px;
}
.footer p { margin-bottom: 4px; }
.footer .license { font-family: Arial, sans-serif; font-size: 11.5px; margin-top: 10px; }

/* ── FIGURES (inline charts) ── */
figure.chart-container { margin: 26px 0; padding: 18px 22px; text-align: center; break-inside: avoid; }
figure.chart-container img { max-width: 100%; height: auto; }
figure.chart-container figcaption {
    margin-top: 10px; font-size: 13px; color: #4a5a6a; text-align: left; font-weight: 400;
}

/* ── INTRO NOTE + TABLE OF CONTENTS ── */
.toc { margin: 0 0 28px; padding: 0; }
.toc h2 { margin: 0 0 12px; font-size: 22px; color: var(--blue); font-weight: 400; }
.toc ol { list-style: none; padding: 0; margin: 0; }
.toc li { margin: 0; padding: 7px 0; border-bottom: 1px dotted var(--rule); font-size: 15px; }
.toc li.sub { padding-left: 22px; font-size: 14px; }
.toc a { color: var(--navy); text-decoration: none; }
.toc a:hover { color: var(--blue); }

/* ── PRINT ── */
@media print {
    .download-bar { display: none; }
    body { font-size: 12.5px; }
    .cover { min-height: 100vh; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .content { padding: 30px 20px; }
    h1 { page-break-before: always; font-size: 24px; }
    h1:first-child { page-break-before: avoid; }
    .stat-card, .phase, .chart-container, .swot-card, table { break-inside: avoid; }
    thead th, .verdict, .phase-badge, .swot-card, .callout {
        -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }
}
@media (max-width: 700px) {
    .swot-grid { grid-template-columns: 1fr; }
    .content { padding: 36px 20px; }
    .cover-brand { position: static; margin-top: 40px; }
}
"""

COVER = """<!-- ═══ COVER PAGE ═══ -->
<div class="download-bar">
    <a class="download-btn" href="@@DOCX@@" download title="Download this report as a Word document">
        <svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg>
        Download Word report
    </a>
</div>
<div class="cover">
    <div class="cover-draft">DO NOT PUBLISH – INTERNAL DOCUMENT</div>
    <div class="cover-date">{date}</div>
    <div class="cover-country">Internet Resilience in @@COUNTRY_NAME@@</div>
    <div class="cover-title">@@TOPIC@@ diagnostics report and action plan</div>
    <div class="cover-meta">
        @@SOURCES@@<br>
        Framework: ISOC Internet Resilience Index<br>
        ISOC Pulse
        <br>
        <a class="download-btn large" href="@@DOCX@@" download>
            <svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg>
            Download Word report (.docx)
        </a>
    </div>
    <div class="cover-brand">Internet<br>Society</div>
</div>

"""

MERMAID_ISOC = (
    "<script>mermaid.initialize({{startOnLoad: true, theme: 'default', themeVariables: {{ "
    "'fontFamily': 'Hind, Arial, sans-serif', "
    + ", ".join(f"'pie{i+1}': '#{c}'" for i, c in enumerate(
        [BRIGHT_BLUE, DEEP_INDIGO, TEAL, CORAL, GOLD, PLUM, "7FA9E8", "8C9BC4", "5C6F8F", "B3C7E6", "26867A", "A9402B"]))
    + ", 'xyChart': {{ 'backgroundColor': '#ffffff', 'titleColor': '#" + DEEP_INDIGO + "', "
    "'xAxisLabelColor': '#" + DARK_NAVY + "', 'yAxisLabelColor': '#" + DARK_NAVY + "', "
    "'plotColorPalette': '#" + BRIGHT_BLUE + ", #" + DEEP_INDIGO + ", #" + TEAL + ", #" + CORAL + "' }} }} }});</script>"
)


@lru_cache(maxsize=1)
def _cover_data_uri():
    """Cover photo from the template docx, shrunk and base64-embedded (HTML stays one file)."""
    try:
        from PIL import Image
        with zipfile.ZipFile(TEMPLATE_DOCX) as z:
            raw = z.read("word/media/image2.jpg")
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.thumbnail((1100, 1500))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=72, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def _braces(s):
    """Escape for str.format()."""
    return s.replace("{", "{{").replace("}", "}}")


def apply_isoc_theme(template, topic_title, docx_filename, country_code,
                     sources="Data Sources: ISOC Pulse API · Internet Yellow Pages (IYP)",
                     semantic_pies=False):
    from docx_builder import country_name

    css = CSS.replace("@@COVER_IMG@@", _cover_data_uri())
    style = "<style>\n" + _braces(css) + "\n    </style>"
    out = re.sub(r"<style>.*?</style>", lambda m: style, template, count=1, flags=re.S)

    out = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Inter[^>]*>',
                 lambda m: FONT_LINK, out, count=1)

    cover = (COVER.replace("@@DOCX@@", docx_filename)
                  .replace("@@COUNTRY_NAME@@", country_name(country_code))
                  .replace("@@TOPIC@@", topic_title)
                  .replace("@@SOURCES@@", sources))
    out = re.sub(r"<!-- ═══ COVER PAGE ═══ -->.*?(?=<!-- ═══ REPORT BODY)",
                 lambda m: cover, out, count=1, flags=re.S)

    # footer: keep the credits, add the licence line used in the Word report's footer
    out = re.sub(r"(<p>Team:[^<]*</p>)",
                 lambda m: m.group(1) + '\n        <p class="license">internetsociety.org · @internetsociety · CC BY-NC-SA 4.0</p>',
                 out, count=1)

    if not semantic_pies:
        out = re.sub(r"<script>mermaid\.initialize\(.*?</script>",
                     lambda m: MERMAID_ISOC, out, count=1, flags=re.S)
    return out


def prepare_html_content(llm_html):
    """Turn the LLM body into the final web content.

    - isoc-chart JSON blocks -> inline PNG <figure> with numbered captions (same renderer as the Word file)
    - adds the single "How to interpret the numbers" note and a clickable table of contents
    - gives every h1/h2 an id for the TOC links
    """
    import html as _html
    from bs4 import BeautifulSoup
    from docx_charts import parse_chart_json, render_chart
    from isoc_report import INTRO_NOTE

    soup = BeautifulSoup(llm_html, "html.parser")

    fig_no = 0
    for div in soup.select("div.isoc-chart"):
        try:
            spec = parse_chart_json(div.get_text())
        except Exception:
            div.decompose()
            continue
        png = render_chart(spec)
        if not png:
            div.decompose()
            continue
        with open(png, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        os.remove(png)
        fig_no += 1
        cap = _html.escape(spec.get("caption") or spec.get("title") or "Chart")
        alt = _html.escape(spec.get("title") or "Chart")
        spec_attr = _html.escape(div.get_text().strip(), quote=True)
        fig = BeautifulSoup(
            f'<figure class="chart-container" data-chart-spec="{spec_attr}"><img alt="{alt}" src="data:image/png;base64,{b64}">'
            f'<figcaption><strong>Figure {fig_no}.</strong> {cap}</figcaption></figure>', "html.parser")
        div.replace_with(fig)

    toc_items = []
    for i, h in enumerate(soup.find_all(["h1", "h2"])):
        h["id"] = f"sec-{i}"
        toc_items.append((h.name, h.get_text(" ", strip=True), h["id"]))

    toc_html = "".join(
        f'<li class="{"sub" if tag == "h2" else ""}"><a href="#{hid}">{_html.escape(txt)}</a></li>'
        for tag, txt, hid in toc_items)
    intro = BeautifulSoup(
        '<div class="toc"><h2>Table of contents</h2><ol>' + toc_html + "</ol></div>"
        '<div class="callout"><strong>How to interpret the numbers in this report?</strong> <br>'
        + _html.escape(INTRO_NOTE) + "</div>", "html.parser")
    body = str(soup)
    return str(intro) + body
