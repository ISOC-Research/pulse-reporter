"""
build_template.py
=================
One-off script that derives templates/ISOC_Template.docx from the official
ISOC_Sample.docx (Amreesh's reference report).

The cover page, headers/footers, page setup, styles and theme are preserved.
The Somalia-specific body is removed, country/topic/date become placeholders
({COUNTRY}, {TOPIC}, {DATE}), and a fresh Table-of-Contents field is inserted.

Usage:
    python build_template.py [path/to/ISOC_Sample.docx]
"""
import copy
import os
import sys

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SAMPLE = os.path.join(HERE, "..", "..", "ISOC_Documents", "ISOC_Sample.docx")
OUT = os.path.join(HERE, "templates", "ISOC_Template.docx")

REPLACEMENTS = [
    ("September 2026", "{DATE}"),
    ("Internet Resilience in Somalia – Diagnostics report", "Internet Resilience in {COUNTRY} – {TOPIC} report"),
    ("Internet Resilience in Somalia", "Internet Resilience in {COUNTRY}"),
    ("Diagnostics report and action plan", "{TOPIC} diagnostics report and action plan"),
    ("Document Title", "Internet Resilience in {COUNTRY} – {TOPIC} report"),
]


def _replace_in_element(root):
    for t in root.iter(qn("w:t")):
        if not t.text:
            continue
        for old, new in REPLACEMENTS:
            if old in t.text:
                t.text = t.text.replace(old, new)
        # normalise en-dash encodings that can differ in the source file
        if "Diagnostics report" in (t.text or "") and "{COUNTRY}" in t.text:
            t.text = "Internet Resilience in {COUNTRY} – {TOPIC} report"


def _toc_paragraphs():
    """Heading + TOC field (Word refreshes it when the file is opened)."""
    head = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    sp = OxmlElement("w:spacing")
    sp.set(qn("w:after"), "200")
    ppr.append(sp)
    head.append(ppr)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    for tag, val in (("w:color", "3A82E4"), ("w:sz", "36"), ("w:szCs", "36")):
        e = OxmlElement(tag)
        e.set(qn("w:val"), val)
        rpr.append(e)
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:asciiTheme"), "majorHAnsi")
    fonts.set(qn("w:hAnsiTheme"), "majorHAnsi")
    rpr.insert(0, fonts)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = "Table of contents"
    r.append(t)
    head.append(r)

    p = OxmlElement("w:p")

    def fld(kind, dirty=False):
        r = OxmlElement("w:r")
        f = OxmlElement("w:fldChar")
        f.set(qn("w:fldCharType"), kind)
        if dirty:
            f.set(qn("w:dirty"), "true")
        r.append(f)
        return r

    p.append(fld("begin", dirty=False))
    r = OxmlElement("w:r")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = ' TOC \\o "1-2" \\h \\z \\u '
    r.append(it)
    p.append(r)
    p.append(fld("separate"))
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "Right-click here and choose “Update field” to refresh the table of contents."
    r.append(t)
    p.append(r)
    p.append(fld("end"))
    return head, p


def main():
    sample = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SAMPLE)
    d = docx.Document(sample)
    body = d.element.body
    kids = list(body)

    # indices from inspection of ISOC_Sample.docx:
    # 0-5 cover (+ section break), 6-33 TOC, 34 "How to interpret" callout, 35+ body, last = sectPr
    keep_front = kids[:6]
    callout = kids[34]
    final_sectpr = kids[-1]
    for k in kids[6:]:
        if k is callout or k is final_sectpr:
            continue
        body.remove(k)

    head, tocp = _toc_paragraphs()
    callout.addprevious(head)
    callout.addprevious(tocp)

    # placeholders: body + every header/footer part
    _replace_in_element(body)
    for sec in d.sections:
        for part in (sec.header, sec.first_page_header, sec.even_page_header,
                     sec.footer, sec.first_page_footer, sec.even_page_footer):
            _replace_in_element(part._element)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.save(OUT)
    print(f"Template written: {OUT}")


if __name__ == "__main__":
    main()
