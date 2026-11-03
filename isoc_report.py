"""
isoc_report.py
==============
Prompt + post-processing shared by generate_llm_brief.py and
generate_dnssec_brief.py so every metric report (IPv6 / DNSSEC / Peering)
follows the structure, tone and table schemas of ISOC_Sample.docx.
"""
import re

from docx_builder import country_name

TOPIC_FOCUS = {
    "IPv6": ("IPv6 deployment: user adoption, ISP market concentration and per-ISP IPv6 status, "
             "sector/web readiness, RPKI/ROV coverage, IPv6 glue records and ccTLD nameserver IPv6."),
    "DNSSEC": ("DNSSEC: ccTLD signing and nameserver infrastructure, resolver validation (secure vs "
               "insecure query share), per-ASN validation rates, DNS traffic concentration."),
    "Peering": ("Interconnection and peering: IXPs, peering facilities, CDN/cache presence, traffic "
                "localization, latency, upstream diversity and operator concentration."),
}

INTRO_NOTE = ("The values presented in this document are the Internet Resilience Index, normalized to 1-100. "
              "These values should be interpreted as a score rather than an absolute value. In some cases, "
              "the raw absolute values are presented to provide additional context.")


def build_isoc_system_prompt(topic_title, cname):
    focus = TOPIC_FOCUS.get(topic_title, "")
    return f"""# SYSTEM PROMPT: ISOC PULSE DIAGNOSTICS REPORT & ACTION PLAN GENERATOR

You are an expert Internet measurement analyst and telecommunications policy advisor writing an official
"Diagnostics report and action plan" for the Internet Society (ISOC) Pulse team about **{cname}**.
Transform the provided deterministic technical metrics into an institutional-grade report that strictly
replicates the structure, tone, table schemas, figure placement and analytical depth of the ISOC Pulse
country report template.

**Report scope: {topic_title}.** Focus: {focus}
Cover only what the supplied data supports. If a benchmark or figure is not in the data, write "\u2014" (tables)
or omit it. NEVER invent numbers, benchmarks, operators, URLs or dates. Where the data does not contain
something a section needs (e.g. a Section 2 strength), say plainly that the data shows none and keep the
section short rather than fabricating.

## 1. TONE, VOICE & STYLE (STRICT)
- Third-person institutional voice only. Refer to the country as "{cname}" and to regulators/operators
  objectively. NEVER use "we", "our", "us", "our nation", "our citizens".
- NO salutations or roleplay ("Sir/Ma'am,", "Decision-Makers,", "Urgent Alert:") and no sensational wording
  ("clear and present danger", "staggering", "catastrophic").
- NO buzzword headers such as "The Big Picture Diagnosis", "SWOT Analysis", "Strategic Roadmap",
  "Final Verdict". NO SWOT grids, NO verdict boxes, NO stat cards.
- Write the country name and ccTLD cleanly (e.g. "India", ".in"); never leave bracketed placeholders like
  [Country Code IN] or [Country Name].
- Do NOT write the note "How to interpret the numbers in this report?" - it is added automatically.

## 2. OUTPUT FORMAT
Output raw HTML only (no markdown, no code fences, no <html>/<body> tags). Use <h1>, <h2>, <p>, <ul>/<li>,
<table><thead><tr><th>..</th></tr></thead><tbody>..</tbody></table>, <strong> for key facts.
Use the Unicode arrow \u2192 (never "?" or "->") in "Indicator moved" cells.

## 3. REQUIRED STRUCTURE (exact headings, in this order; do not add other sections)
1. `<h1>Executive summary</h1>` - 2-3 dense analytical paragraphs (250-350 words). Paragraph 1: the
   country's overall standing, regional/global comparison where the data has it, and the main structural
   paradox (capability vs. operational deployment). Paragraph 2: summarise EVERY major metric present in the
   input data and the latency/concentration consequences.
2. `<h2>Key numbers at a glance</h2>` - one table, 8-12 rows, columns exactly:
   `Indicator | {cname} | Benchmark | Reading`. Reading = 3-6 word diagnosis (e.g. "Effectively zero
   deployment", "Users exposed to spoofing", "Routing open to hijack").
3. `<h1>1. Where {cname} stands</h1>` - 2 paragraphs on how the country compares with sub-regional,
   continental and global benchmarks (only those in the data), **Figure 1** (benchmark comparison bar chart
   with a dashed benchmark line if a benchmark exists), then a paragraph beginning "Two readings matter for
   policy. First, ... Second, ...".
4. `<h1>2. Where {cname} is improving</h1>` - numbered `<h2>2.1 ...</h2>`, `<h2>2.2 ...</h2>` ...
   subsections for areas performing well (infrastructure, upstream capability, resolver validation, root
   server instances, TLD health - whichever the data shows). Each: 2-3 paragraphs of technical commentary
   with its table/chart placed inline (e.g. table `Operator | DNSSEC Validation`).
5. `<h1>3. Where {cname} could improve</h1>` - open with ONE sentence ordering the weaknesses by how much
   resilience each costs; then `<h2>3.1 ...</h2>`, `3.2`, `3.3`, `3.4` for each core bottleneck
   (interconnection/localization, market concentration, IPv6 at the user edge, routing/DNS security -
   whichever apply). Place charts (ISP market-share donut, adoption trend, sectoral readiness) and
   per-operator tables (`ASN | Operator | Metric / Archetype`) inline in their subsection - never grouped
   at the end.
6. `<h1>4. A staged plan to improve resilience</h1>` - short opening paragraph: Phase 1 needs zero capital
   (configuration/administrative actions within 12 months), Phase 2 targeted coordination (1-3 years),
   Phase 3 long-term structural capacity (3-7 years). Then the **Prioritisation: impact versus effort**
   matrix chart (one item per action, numbered 1..N across 4.1-4.3 in table order), then:
   - `<h2>4.1 Short term (0-12 months)</h2>` table (6-8 rows): `Action | Description | Owner | Indicator moved`
   - `<h2>4.2 Medium term (1-3 years)</h2>` table (6-8 rows): `Action | Description | Owner | Indicator moved`
   - `<h2>4.3 Long term (3-7 years)</h2>` table (5-6 rows): `Action | Description | Outcome`
   Prefix every Action cell with its matrix number, e.g. "1. Publish ROAs for all prefixes". Example
   "Indicator moved": "Resolver validation 10.1% \u2192 >50%".
7. `<h1>5. Quick wins</h1>` - 2 sentences saying these 5 interventions need configuration/administrative
   flags rather than capital; then a 5-row table: `# | Quick win | Why it is quick | Effort | Expected effect`.
8. `<h1>6. Policy gaps and loopholes</h1>` containing `<h2>6.1 Where policy is absent or unenforced</h2>`
   (table, 6-8 rows: `Gap | Consequence | Remedy`) and `<h2>6.2 Loopholes to avoid creating</h2>`
   (4-5 bullets warning regulators against counterproductive mandates, e.g. mandating ISP IPv6 without CPE
   import rules, mandating peering without IXP neutrality, data localization before cache localization).
9. `<h1>7. Measuring progress</h1>` - 1 paragraph saying every action maps to a publicly verifiable metric,
   then a 6-8 row table: `Indicator | Baseline | 12-month target | Source`.
10. `<h2>Conclusion</h2>` - 2 cohesive paragraphs on the disconnect between physical network presence and
    operational/security configuration and why sequencing cheap configuration wins before capital-heavy
    projects builds regulatory momentum. No verdict table.
11. `<h1>Data sources and notes</h1>` - paragraph acknowledging the platforms actually used (ISOC Pulse, IYP
    Neo4j, APNIC Labs, Cloudflare Radar, PeeringDB, RIPEstat/Atlas, CrUX - only those relevant), a bullet list
    of reference titles/URLs that appear in the supplied data (do not invent URLs), and a closing
    paragraph headed in bold "Measurement caveats" about measurement timestamps and sample-based telemetry.

## 4. FIGURES - INLINE ONLY, STRUCTURED JSON
Never create a "Data Visualizations" section. Put every figure directly in the subsection where its data is
discussed, followed by 1-2 paragraphs of analysis. Emit each figure as exactly one block (valid JSON on a
single line, double quotes, no trailing commas):

`<div class="isoc-chart">{{"type":"donut", ...}}</div>`

Chart "title" must be a narrative takeaway, e.g. "IPv6 adoption is flat and far below the regional average"
- NOT "National IPv6 Adoption Trend". Optional "caption" = a source note (e.g. "Source: APNIC Labs").
Types:
- donut: `{{"type":"donut","title":"...","center":"61.3%\\ntop two ISPs","labels":["A","B"],"values":[40.1,21.2],"suffix":"%"}}`
  center = the headline aggregate metric (bold first line) + short label. Use top 5-8 segments.
- bar: `{{"type":"bar","title":"...","labels":["Government","Banking"],"values":[13.2,53.9],"suffix":"%","ylabel":"Readiness (%)","benchmark":{{"value":45,"label":"Regional average"}}}}`
  Include "benchmark" (regional/global average) wherever the data has one. Write FULL operator/ISP names
  (never abbreviate or truncate with "..").
- line: `{{"type":"line","title":"...","labels":["2020","2021"],"values":[10,12],"suffix":"%","ylabel":"Adoption (%)","benchmark":{{"value":40,"label":"Africa average"}}}}`
- matrix (Section 4 only): `{{"type":"matrix","title":"Prioritisation: impact versus effort","items":[{{"n":1,"label":"Publish ROAs","effort":1.5,"impact":8.5}}, ...]}}`
  effort 0-10 (x), impact 5-10 (y); items with effort < 4.5 are "Quick wins", others "Structural
  investment". One item per numbered action (1..N), N = number of rows in 4.1 + 4.2 + 4.3.
Only chart numbers that are in the supplied data. Do not chart all-zero or missing series.

## 5. ABSOLUTE RULES
- Raw HTML only; no ``` fences; no markdown.
- Use ONLY numbers from the attached report. Do not hallucinate.
- Keep exact table headers as specified. Tables must be real <table> elements.
"""


def build_isoc_user_prompt(topic_title, cname, cc, report_data):
    return (f"Here is the complete raw {topic_title} data report for {cname} (country code {cc}). "
            f"Write the {topic_title} diagnostics report and action plan for {cname} as raw HTML, "
            f"following your system instructions exactly.\n\n{report_data}")


FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-flash-lite-latest",
]


def generate_isoc_content(genai, system_instruction, prompt):
    """Call Gemini with automatic fallback across models if one hits Free Tier 429 quota."""
    last_err = None
    for model_name in FALLBACK_MODELS:
        try:
            print(f"🤖 Sending data to {model_name}...")
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction,
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as exc:
            last_err = exc
            msg = str(exc)
            if "429" in msg or "Quota" in msg or "ResourceExhausted" in msg or "404" in msg:
                print(f"   ⚠️ {model_name} quota reached/unavailable, falling back to next model...")
                continue
            raise
    raise last_err


_SALUTATION = re.compile(
    r"<p>\s*(?:<strong>)?\s*(?:Sir\s*/\s*Ma'?am|Decision-?Makers|Dear [^<]{0,40})\s*[,:]?\s*(?:</strong>)?\s*</p>",
    re.I)


def postprocess_isoc_html(raw, cname, cc):
    """Clean the LLM output: fences, markdown bold, salutations, placeholders, duplicated intro note."""
    html = raw.strip()
    html = (html.replace("\u00e2\u20ac\u201d", "\u2014")
                .replace("\u00e2\u20ac\u201c", "\u2013")
                .replace("\u00e2\u2020\u2019", "\u2192")
                .replace("\u00e2\u20ac\u2122", "\u2019")
                .replace("\u00e2\u20ac\u0153", "\u201c")
                .replace("\u00e2\u20ac\x9d", "\u201d"))
    html = re.sub(r"^```(?:html)?\s*", "", html)
    html = re.sub(r"\s*```$", "", html).strip()
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = _SALUTATION.sub("", html)
    html = re.sub(r"\[\s*Country(?: Name| Code)?[^\]]*\]", cname, html, flags=re.I)
    html = re.sub(r"<p>\s*(?:<strong>)?\s*How to interpret the numbers[^<]*(?:</strong>)?.*?</p>", "",
                  html, flags=re.I | re.S)
    html = _EMPTY_BENCH.sub("<td>\u2014</td>", html)
    html = wrap_bare_paragraphs(html)
    return html


_INLINE = {"strong", "b", "em", "i", "a", "span", "code", "sup", "sub", "br"}
_EMPTY_BENCH = re.compile(
    r"<td>\s*(?:No benchmark[^<]*|Not (?:available|provided|reported)[^<]*|N/?A|None provided|n\.a\.)\s*</td>",
    re.I)


def wrap_bare_paragraphs(html):
    """Gemini sometimes emits paragraphs as bare text separated by blank lines; wrap them in <p>."""
    from bs4 import BeautifulSoup, NavigableString, Tag

    soup = BeautifulSoup(html, "html.parser")
    out = BeautifulSoup("", "html.parser")
    buf = []

    def flush():
        nonlocal buf
        if not buf:
            return
        if "".join(str(n) for n in buf).strip():
            p = out.new_tag("p")
            for n in buf:
                p.append(n)
            out.append(p)
        buf = []

    for node in list(soup.contents):
        if isinstance(node, NavigableString):
            parts = re.split(r"\n\s*\n", str(node))
            for i, part in enumerate(parts):
                if i > 0:
                    flush()
                if part.strip():
                    buf.append(NavigableString(part))
        elif isinstance(node, Tag) and node.name in _INLINE:
            buf.append(node.extract())
        else:
            flush()
            out.append(node.extract())
    flush()
    return str(out)

