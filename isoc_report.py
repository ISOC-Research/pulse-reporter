"""
isoc_report.py
==============
Prompt + post-processing shared by generate_llm_brief.py so every metric report
(IPv6 / DNSSEC / Peering) follows the structure, tone and table schemas of
ISOC_Sample.docx and enforces the 6 strict quality-control & consistency rules.
"""
import json
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

INTRO_NOTE = ("The values presented in this document are the Internet Resilience Index, normalized to 1\u2013100. "
              "These values should be interpreted as a score rather than an absolute value. In some cases, "
              "the raw absolute values are presented to provide additional context.")


def build_isoc_system_prompt(topic_title, cname, cc=""):
    focus = TOPIC_FOCUS.get(topic_title, "")
    cc_upper = (cc or "").upper() or "CC"
    cc_lower = cc_upper.lower()
    return f"""# SYSTEM PROMPT: ISOC PULSE DIAGNOSTICS REPORT & ACTION PLAN GENERATOR

You are an expert Internet measurement analyst and telecommunications policy advisor writing an official
"Diagnostics report and action plan" for the Internet Society (ISOC) Pulse team about **{cname}** ({cc_upper}).
Transform the provided deterministic technical metrics into an institutional-grade report that strictly
replicates the structure, tone, table schemas, figure placement and analytical depth of the ISOC Pulse
country report template.

**Report scope: {topic_title}.** Focus: {focus}
Cover only what the supplied data supports. NEVER invent country numbers, operators or dates. Where the data
does not contain something a section needs, state plainly what the data shows and keep the section concise.

## 1. TONE, VOICE & STYLE (STRICT)
- Third-person institutional voice only. Refer to the country as "{cname}" and to regulators/operators
  objectively. NEVER use "we", "our", "us", "our nation", "our citizens".
- NO salutations or roleplay ("Sir/Ma'am,", "Decision-Makers,", "Urgent Alert:") and no sensational wording
  ("clear and present danger", "staggering", "catastrophic").
- NO buzzword headers such as "The Big Picture Diagnosis", "SWOT Analysis", "Strategic Roadmap",
  "Final Verdict". NO SWOT grids, NO verdict boxes, NO stat cards.
- Write the country name and ccTLD cleanly (e.g. "{cname}", ".{cc_lower}"); never leave bracketed placeholders
  like [Country Code] or [Country Name].
- Do NOT write the note "How to interpret the numbers in this report?" - it is added automatically once
  above the Executive Summary.

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
   deployment", "Strong CDN cache footprint", "Suboptimal local peering").
   **BENCHMARK RULE**: Do NOT leave the entire `Benchmark` column filled with em-dashes (`\u2014`). While raw
   national counts (such as total routed ASNs or total IXP count) may use `\u2014`, any percentage, ratio, CDN
   count, HHI index, or latency indicator MUST include a regional/global benchmark from the data or an ISOC
   best-practice reference threshold (e.g., `9 of 9 global` for Tier-1 CDNs, `>50% target` for Traffic
   Localization Ratio and Domestic IXP Penetration Rate, `100% of active IXPs` for IXP Telemetry Reporting,
   `<0.15 diversified` for Geographic Concentration HHI, `0% ideal` for Domestic Tromboning Rate,
   `<20 ms target` for Median Eyeball Edge Latency, `<50 ms target` for P95 Latency, `100% target` for RPKI/DNSSEC/IPv6).
3. `<h1>1. Where {cname} stands</h1>` - 2 paragraphs on how the country compares with sub-regional,
   continental and global/reference benchmarks, **Figure 1** (benchmark comparison bar chart with a dashed
   benchmark line), then a paragraph beginning "Two readings matter for policy. First, ... Second, ...".
4. `<h1>2. Where {cname} is improving</h1>` - numbered `<h2>2.1 ...</h2>`, `<h2>2.2 ...</h2>` ...
   subsections for areas performing well. Each: 2 paragraphs of technical commentary with a unique,
   multi-column table or chart placed inline.
5. `<h1>3. Where {cname} could improve</h1>` - open with ONE sentence ordering the weaknesses by how much
   resilience each costs; then `<h2>3.1 ...</h2>`, `3.2`, `3.3`, `3.4` for each core bottleneck.
   **ZERO DUPLICATE TABLES RULE**: NEVER repeat `Indicator | Value` summary rows in Section 2 or Section 3
   that were already shown in `Key numbers at a glance` or earlier tables (e.g. do NOT create a 2-column
   table repeating `Active Routed Domestic ASNs`, `Domestic ASNs Peering at Local IXPs`, `Domestic IXP
   Penetration Rate`, or `Localization Ratio`). Instead, every table in Sections 2 and 3 MUST be a
   **multi-column granular breakdown** (at least 3-4 columns) using the detailed breakdown tables in the
   supplied raw report (such as City-by-City IXP Hub Distribution, IXP Traffic Telemetry Reporting Breakdown,
   Top Unpeered Domestic ASNs, Tier-1 CDN Presence Matrix, Latency Percentile Breakdown, or Per-Operator/Per-ASN
   compliance tables).
6. `<h1>4. A staged plan to improve resilience</h1>` - short opening paragraph: Phase 1 needs zero capital
   (configuration/administrative actions within 12 months), Phase 2 targeted coordination (1-3 years),
   Phase 3 long-term structural capacity (3-7 years). Then the **Prioritisation: impact versus effort**
   matrix chart, then:
   - `<h2>4.1 Short term (0\u201312 months)</h2>` table (**EXACTLY 5 rows**, numbered `1.` to `5.`):
     `Action | Description | Owner | Indicator moved`
   - `<h2>4.2 Medium term (1\u20133 years)</h2>` table (**3 rows**, numbered `6.` to `8.`):
     `Action | Description | Owner | Indicator moved`
   - `<h2>4.3 Long term (3\u20137 years)</h2>` table (**2 rows**, numbered `9.` to `10.`):
     `Action | Description | Outcome`
   Prefix every Action cell with its matrix number, e.g. `1. Launch targeted IXP onboarding campaign`.
   Example `Indicator moved`: `Domestic ASN IXP Penetration Rate 27.19% \u2192 >35%`.
7. `<h1>5. Quick wins</h1>` - 2 sentences stating that these **five interventions** require configuration or
   administrative coordination rather than capital; then a **5-row table** (numbered `1` to `5`, matching
   the EXACT 5 actions from Section 4.1):
   `# | Quick win | Why it is quick | Effort | Expected effect`.
   **SECTION 5 EFFORT & EFFECT RULE**:
   - NEVER write generic words like `"Low"`, `"Medium"`, or `"High"` in the `Effort` column.
   - Populate `Effort` with concrete operational timeframes matching the ISOC style (e.g., `"2\u20134 weeks of IXP outreach"`,
     `"Days of operator work"`, `"Hours per network"`, `"One maintenance window per member"`, `"1\u20132 weeks of registry coordination"`).
   - In `Expected effect`, ALWAYS include the measurable baseline-to-target shift matching Section 4.1 (e.g.,
     `"Raise domestic ASN IXP penetration from 27.19% to >35%"` rather than vague statements like `"Increased IXP membership"`).
8. `<h1>6. Policy gaps and loopholes</h1>` containing `<h2>6.1 Where policy is absent or unenforced</h2>`
   (table, 4-6 rows: `Gap | Consequence | Remedy`) and `<h2>6.2 Loopholes to avoid creating</h2>`
   (4-5 bullets warning regulators against counterproductive mandates).
9. `<h1>7. Measuring progress</h1>` - 1 paragraph saying every action maps to a publicly verifiable metric,
   then a 5-8 row table: `Indicator | Baseline | 12-month target | Source`.
10. `<h2>Conclusion</h2>` - 2 cohesive paragraphs on the disconnect between physical network presence and
    operational/security configuration and why sequencing cheap configuration wins before capital-heavy
    projects builds regulatory momentum. No verdict table.
11. `<h1>Data sources and notes</h1>` - paragraph acknowledging the platforms actually used, followed by a
    `<ul>` bullet list of **country-specific deep links** (NEVER generic root homepages like `https://stat.ripe.net/`
    or `https://www.peeringdb.com/`). Include the relevant country-specific deep links from this list:
    - `ISOC Pulse \u2014 Country Report for {cname}: https://pulse.internetsociety.org/en/reports/{cc_lower}/`
    - `ISOC Pulse \u2014 Internet Resilience Index for {cname}: https://pulse.internetsociety.org/en/resilience/{cc_lower}/`
    - `RIPEstat \u2014 Country ASNs & Routing Status for {cc_upper}: https://stat.ripe.net/{cc_upper}`
    - `PeeringDB \u2014 IXP & Facility Directory for {cc_upper}: https://www.peeringdb.com/advanced_search?country={cc_upper}`
    - `RIPE Atlas \u2014 Active Probes & Anchors in {cc_upper}: https://atlas.ripe.net/probes/?country={cc_upper}`
    - `Packet Clearing House (PCH) \u2014 IXP Directory: https://www.pch.net/ixp/dir`
    Then close with a paragraph headed in bold `<strong>Measurement caveats.</strong>` about measurement timestamps
    and sample-based telemetry.

## 4. FIGURES - INLINE ONLY, STRUCTURED JSON
Never create a "Data Visualizations" section. Put every figure directly in the subsection where its data is
discussed, followed by 1-2 paragraphs of analysis. Emit each figure as exactly one block (valid JSON on a
single line, double quotes, no trailing commas):

`<div class="isoc-chart">{{"type":"donut", ...}}</div>`

Chart "title" must be a narrative takeaway - NOT a generic label. Optional "caption" = source note.
Types:
- donut: `{{"type":"donut","title":"...","center":"27.19%\\npeered at IXPs","labels":["Peered at local IXP","Unpeered domestic ASNs"],"values":[27.19,72.81],"suffix":"%"}}`
  **DONUT CENTER RULE**: Always format `"center"` as two lines separated by `\\n`: Line 1 = primary metric/ratio/percentage ONLY (e.g. `"8 of 9"`, `"18 of 32"`, `"27.19%"`, `"86.63%"`); Line 2 = short unit/descriptor (e.g. `"Tier-1 CDNs"`, `"reporting IXPs"`, `"peered at IXPs"`, `"utilization"`).
- bar: `{{"type":"bar","title":"...","labels":["Mumbai","Chennai"],"values":[10,5],"suffix":"","ylabel":"Operational IXPs","benchmark":{{"value":50,"label":"Target"}}}}`
  **BENCHMARK LABEL RULE**: Use a plain label like `"Target"` or `"Regional average"` in `"benchmark.label"` (do NOT duplicate the numeric value inside parentheses in `"label"` since the chart renderer appends the value automatically).
- line: `{{"type":"line","title":"...","labels":["2020","2021"],"values":[10,12],"suffix":"%","ylabel":"Adoption (%)"}}`
- matrix (Section 4 only): `{{"type":"matrix","title":"Prioritisation: impact versus effort","items":[{{"n":1,"label":"...","effort":1.8,"impact":8.8}}, ...]}}`
  **STRICT MATRIX ALIGNMENT RULE**:
  - Items `1` through `5` MUST map to the 5 Short-Term/Quick-Win actions (Section 4.1 & Section 5) and have `effort < 4.5` (e.g. `1.2`, `1.8`, `2.4`, `3.0`, `3.6`) so they plot strictly inside the green `QUICK WINS` zone.
  - Items `6` through `10` MUST map to the Medium-Term (Section 4.2, items `6`–`8`) and Long-Term (Section 4.3, items `9`–`10`) actions and have `effort > 4.5` (e.g. `5.2`, `6.0`, `6.8`, `8.0`, `8.8`) so they plot strictly inside the `STRUCTURAL INVESTMENT` zone.
Only chart numbers that are in the supplied data. Do not chart all-zero or missing series.

## 5. ABSOLUTE RULES
- Raw HTML only; no ``` fences; no markdown.
- Use ONLY country metrics from the attached report. Do not hallucinate.
- Keep exact table headers as specified. Tables must be real <table> elements.
"""


def build_isoc_user_prompt(topic_title, cname, cc, report_data):
    return (f"Here is the complete raw {topic_title} data report for {cname} (country code {cc}). "
            f"Write the {topic_title} diagnostics report and action plan for {cname} as raw HTML, "
            f"following your system instructions and all 6 quality control rules exactly.\n\n{report_data}")


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

_INLINE = {"strong", "b", "em", "i", "a", "span", "code", "sup", "sub", "br"}
_EMPTY_BENCH = re.compile(
    r"<td>\s*(?:No benchmark[^<]*|Not (?:available|provided|reported)[^<]*|N/?A|None provided|n\.a\.)\s*</td>",
    re.I)

# Concrete operational effort phrases for Section 5 (Quick wins) when LLM outputs generic "Low"/"Medium"
_DEFAULT_EFFORTS = [
    "2\u20134 weeks of IXP outreach",
    "Days of operator work",
    "Hours per network",
    "One maintenance window per member",
    "1\u20132 weeks of administrative review",
]

# Reference benchmarks for "Key numbers at a glance" when the LLM leaves "\u2014" on a non-count indicator
_BENCHMARK_RULES = [
    (re.compile(r"tier-?1.*cdn|global.*cdn|cdn.*presence", re.I), "9 of 9 global"),
    (re.compile(r"ixp.*penetration|peering.*penetration|domestic.*asn.*peering.*rate", re.I), ">50% target"),
    (re.compile(r"locali[sz]ation\s*ratio|traffic\s*locali[sz]ation", re.I), ">50% target"),
    (re.compile(r"tromboning", re.I), "0% ideal"),
    (re.compile(r"median.*latency|eyeball.*latency|edge.*latency", re.I), "<20 ms target"),
    (re.compile(r"95th|p95.*latency|tail.*latency", re.I), "<50 ms target"),
    (re.compile(r"hhi|geographic\s*concentration", re.I), "<0.15 diversified"),
    (re.compile(r"reporting\s*traffic|traffic\s*telemetry|pch.*reporting", re.I), "100% of active IXPs"),
    (re.compile(r"rpki|roa|rov", re.I), "100% target"),
    (re.compile(r"ixp.*ipv6.*lan", re.I), "100% target"),
    (re.compile(r"ixp.*member.*ipv6", re.I), ">80% target"),
    (re.compile(r"government.*ipv6|gov.*readiness", re.I), "100% target"),
    (re.compile(r"glue.*record", re.I), "100% target"),
    (re.compile(r"authoritative.*nameserver|nameserver.*ipv6", re.I), "100% target"),
    (re.compile(r"dnssec.*validation|secure.*query|resolver.*validation", re.I), "100% target"),
    (re.compile(r"underserved.*market|non-?compliant.*isp", re.I), "0% ideal"),
]


def _cell_text(cell):
    return re.sub(r"\s+", " ", cell.get_text(" ", strip=True)).strip()


def _strip_num_prefix(text):
    return re.sub(r"^\s*\d+[\.\)]\s*", "", text or "").strip()


def _populate_reference_benchmarks(soup):
    """Rule 5: Ensure 'Key numbers at a glance' populates reference thresholds for ratios/percentages/latency."""
    for tbl in soup.find_all("table"):
        ths = [_cell_text(th).lower() for th in tbl.find_all("th")]
        if len(ths) == 4 and "indicator" in ths[0] and "benchmark" in ths[2]:
            tbody = tbl.find("tbody") or tbl
            for tr in tbody.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 4:
                    continue
                ind = _cell_text(tds[0])
                val = _cell_text(tds[1])
                bench = _cell_text(tds[2])
                if bench in ("", "\u2014", "-", "--", "N/A", "n/a"):
                    # Match specific indicator rules first
                    matched = None
                    for pat, ref in _BENCHMARK_RULES:
                        if pat.search(ind):
                            matched = ref
                            break
                    # Fallback if value is a percentage or ms and still unmatched
                    if not matched:
                        if "%" in val and not re.search(r"share of top", ind, re.I):
                            matched = ">50% target"
                        elif "ms" in val.lower():
                            matched = "<20 ms target"
                    if matched:
                        tds[2].string = matched
            break


def _deduplicate_section_tables(soup):
    """Rule 3: Remove duplicate summary rows or repeated rows across Sections 1, 2, and 3."""
    seen_indicators = set()
    seen_row_pairs = set()
    for h in soup.find_all(["h1", "h2"]):
        if _cell_text(h).lower().startswith("4."):
            break
    tables = soup.find_all("table")
    for idx, tbl in enumerate(tables):
        # Stop deduplicating once we reach Section 4 (action tables / measuring progress)
        prev_h1 = tbl.find_previous("h1")
        if prev_h1 and re.match(r"^\s*[4567]\.", _cell_text(prev_h1)):
            break
        ths = [_cell_text(th).lower() for th in tbl.find_all("th")]
        tbody = tbl.find("tbody") or tbl
        rows = [tr for tr in tbody.find_all("tr") if tr.find_all("td")]
        if idx == 0:
            for tr in rows:
                tds = tr.find_all("td")
                if tds:
                    seen_indicators.add(re.sub(r"[^a-z0-9]+", " ", _cell_text(tds[0]).lower()).strip())
            continue

        ncols = max([len(ths)] + [len(tr.find_all("td")) for tr in rows] + [0])
        kept = 0
        for tr in list(rows):
            tds = tr.find_all("td")
            if not tds:
                continue
            c0 = re.sub(r"[^a-z0-9]+", " ", _cell_text(tds[0]).lower()).strip()
            c1 = re.sub(r"[^a-z0-9]+", " ", _cell_text(tds[1]).lower()).strip() if len(tds) > 1 else ""
            if ncols == 2 and (
                c0 in seen_indicators or any(
                    w in c0 for w in (
                        "active routed domestic asns",
                        "domestic asns peering at local ixps",
                        "domestic ixp penetration rate",
                        "localization ratio",
                        "traffic localization ratio",
                    )
                )
            ):
                tr.decompose()
            elif ncols >= 3 and (c0, c1) in seen_row_pairs:
                tr.decompose()
            else:
                seen_indicators.add(c0)
                if ncols >= 3:
                    seen_row_pairs.add((c0, c1))
                kept += 1
        if kept == 0:
            tbl.decompose()


def _enforce_staged_plan_and_quick_wins(soup):
    """Rules 1 & 4:
    - Strictly 5 actions (1..5) in Section 4.1 (Short term)
    - Sequentially numbered actions (6..N) in Section 4.2 (Medium term) and Section 4.3 (Long term)
    - Strictly 5 matching rows (1..5) in Section 5 (Quick wins) with concrete operational Effort and quantified Expected effect
    - Matrix chart synchronized with 1..5 in Quick Wins (effort < 4.5) and 6..N in Structural Investment (effort > 4.5)
    """
    t41 = t42 = t43 = t5 = None
    for h in soup.find_all(["h1", "h2", "h3"]):
        htxt = _cell_text(h).lower()
        nxt_tbl = h.find_next("table")
        if not nxt_tbl:
            continue
        if "4.1" in htxt or "short term" in htxt:
            t41 = nxt_tbl
        elif "4.2" in htxt or "medium term" in htxt:
            t42 = nxt_tbl
        elif "4.3" in htxt or "long term" in htxt:
            t43 = nxt_tbl
        elif htxt.startswith("5.") or "quick wins" in htxt:
            t5 = nxt_tbl

    if not t41:
        return

    b41 = t41.find("tbody") or t41
    r41 = [tr for tr in b41.find_all("tr") if tr.find_all("td")]
    b42 = (t42.find("tbody") or t42) if t42 else None
    r42 = [tr for tr in b42.find_all("tr") if tr.find_all("td")] if b42 else []
    b43 = (t43.find("tbody") or t43) if t43 else None
    r43 = [tr for tr in b43.find_all("tr") if tr.find_all("td")] if b43 else []

    # Balance 4.1 to have strictly 5 rows
    while len(r41) < 5 and len(r42) > 1:
        moved = r42.pop(0)
        b41.append(moved)
        r41.append(moved)
    while len(r41) > 5 and b42 is not None:
        moved = r41.pop()
        b42.insert(0, moved)
        r42.insert(0, moved)

    # Renumber 4.1 (1..5), 4.2 (6..), 4.3 (..)
    all_actions = []  # list of (num, title, desc, owner, indicator_moved, phase_idx)
    counter = 0
    for phase_idx, rows in ((1, r41), (2, r42), (3, r43)):
        for tr in rows:
            tds = tr.find_all("td")
            if not tds:
                continue
            counter += 1
            raw_title = _strip_num_prefix(_cell_text(tds[0]))
            tds[0].clear()
            tds[0].string = f"{counter}. {raw_title}"
            desc = _cell_text(tds[1]) if len(tds) > 1 else ""
            owner = _cell_text(tds[2]) if len(tds) > 3 else ""
            ind_moved = _cell_text(tds[3]) if len(tds) > 3 else (_cell_text(tds[2]) if len(tds) > 2 else "")
            ind_moved = ind_moved.replace("->", "\u2192")
            if len(tds) > 3:
                tds[3].string = ind_moved
            all_actions.append((counter, raw_title, desc, owner, ind_moved, phase_idx))

    # Synchronize Section 5 (Quick wins) to have strictly the 5 actions from 4.1
    if t5 is not None:
        b5 = t5.find("tbody") or t5
        existing_r5 = [tr for tr in b5.find_all("tr") if tr.find_all("td")]
        existing_by_idx = {}
        for i, tr in enumerate(existing_r5):
            tds = tr.find_all("td")
            if len(tds) >= 5:
                existing_by_idx[i + 1] = (
                    _strip_num_prefix(_cell_text(tds[1])),
                    _cell_text(tds[2]),
                    _cell_text(tds[3]),
                    _cell_text(tds[4]),
                )
        # Rebuild exactly 5 rows in Section 5 matching r41 (actions 1..5)
        for tr in existing_r5:
            tr.decompose()

        short_actions = [a for a in all_actions if a[5] == 1][:5]
        for idx, (num, title, desc, owner, ind_moved, _) in enumerate(short_actions):
            old_qw, old_why, old_eff, old_exp = existing_by_idx.get(num, ("", "", "", ""))
            why_txt = old_why if old_why else (
                "Requires administrative coordination and configuration updates on existing infrastructure rather than new capital deployment."
            )
            # Rule 4: Concrete operational timeframe in Effort (never generic Low/Medium/High)
            eff_clean = old_eff.strip()
            if (not eff_clean or re.fullmatch(
                r"(?:very\s+)?(?:low|medium|moderate|high|minimal|easy|small|short|quick)(?:\s+effort)?\.?",
                eff_clean, re.I
            )):
                eff_clean = _DEFAULT_EFFORTS[idx % len(_DEFAULT_EFFORTS)]

            # Rule 4: Quantified baseline-to-target shift in Expected effect
            exp_clean = old_exp.strip().replace("->", "\u2192")
            has_quant = bool(re.search(r"\d", exp_clean))
            if not exp_clean or not has_quant:
                if ind_moved:
                    exp_clean = f"Shift {ind_moved}" if "\u2192" in ind_moved else f"{ind_moved}"
                else:
                    exp_clean = exp_clean or "Measurable improvement in national resilience indicator"
            elif ind_moved and "\u2192" in ind_moved and "\u2192" not in exp_clean and " to " not in exp_clean.lower():
                exp_clean = f"{exp_clean.rstrip('.')} ({ind_moved})"

            tr = soup.new_tag("tr")
            for col_val in (str(num), title, why_txt, eff_clean, exp_clean):
                td = soup.new_tag("td")
                td.string = col_val
                tr.append(td)
            b5.append(tr)

    # Synchronize the Section 4 matrix chart JSON with all_actions (1..5 Quick Wins < 4.5, 6..N Structural > 4.5)
    for div in soup.select("div.isoc-chart"):
        try:
            spec = json.loads(div.get_text().strip(), strict=False)
        except Exception:
            continue
        if str(spec.get("type", "")).lower() != "matrix":
            continue
        old_items = {
            int(re.search(r"\d+", str(it.get("n", i + 1))).group(0)): it
            for i, it in enumerate(spec.get("items", []))
            if re.search(r"\d+", str(it.get("n", i + 1)))
        }
        qw_efforts = [1.4, 2.0, 2.6, 3.2, 3.8]
        qw_impacts = [8.8, 8.2, 7.6, 8.5, 7.9]
        si_efforts = [5.4, 6.2, 7.0, 8.0, 8.8, 9.2]
        si_impacts = [8.4, 7.8, 8.9, 9.2, 8.6, 8.0]
        new_items = []
        for num, title, _, _, _, phase_idx in all_actions:
            prev = old_items.get(num, {})
            raw_eff = float(prev.get("effort", 0) or 0)
            raw_imp = float(prev.get("impact", 0) or 0)
            if num <= 5:
                # Strictly inside QUICK WINS zone (x < 4.5)
                if not (0.8 <= raw_eff <= 4.0):
                    raw_eff = qw_efforts[(num - 1) % len(qw_efforts)]
                if not (5.5 <= raw_imp <= 9.6):
                    raw_imp = qw_impacts[(num - 1) % len(qw_impacts)]
            else:
                # Strictly inside STRUCTURAL INVESTMENT zone (x > 4.5)
                si_idx = num - 6
                if not (5.0 <= raw_eff <= 9.4):
                    raw_eff = si_efforts[si_idx % len(si_efforts)]
                if not (5.5 <= raw_imp <= 9.6):
                    raw_imp = si_impacts[si_idx % len(si_impacts)]
            new_items.append({
                "n": num,
                "label": title,
                "effort": round(raw_eff, 1),
                "impact": round(raw_imp, 1),
            })
        if new_items:
            spec["items"] = new_items
            div.string = json.dumps(spec, ensure_ascii=False)


def _enforce_country_deep_links(soup, cname, cc):
    """Rule 6: Replace generic root URLs in 'Data sources and notes' with country-specific deep links."""
    cc_upper = (cc or "").upper()
    cc_lower = cc_upper.lower()
    if not cc_upper:
        return

    canonical_links = [
        f"ISOC Pulse \u2014 Country Report for {cname}: https://pulse.internetsociety.org/en/reports/{cc_lower}/",
        f"ISOC Pulse \u2014 Internet Resilience Index for {cname}: https://pulse.internetsociety.org/en/resilience/{cc_lower}/",
        f"RIPEstat \u2014 Country ASNs & Routing Status for {cc_upper}: https://stat.ripe.net/{cc_upper}",
        f"PeeringDB \u2014 IXP & Facility Directory for {cc_upper}: https://www.peeringdb.com/advanced_search?country={cc_upper}",
        f"RIPE Atlas \u2014 Active Probes & Anchors in {cc_upper}: https://atlas.ripe.net/probes/?country={cc_upper}",
        "Packet Clearing House (PCH) \u2014 IXP Directory: https://www.pch.net/ixp/dir",
    ]

    for h in soup.find_all(["h1", "h2"]):
        if "data sources" in _cell_text(h).lower():
            ul = h.find_next("ul")
            if ul:
                ul.clear()
                for item in canonical_links:
                    li = soup.new_tag("li")
                    li.string = item
                    ul.append(li)
            break


def postprocess_isoc_html(raw, cname, cc):
    """Clean the LLM output and deterministically enforce all 6 ISOC Quality Control & Consistency Rules."""
    from bs4 import BeautifulSoup

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
    # Rule 2: Strip any LLM-emitted 'How to interpret the numbers' paragraph
    html = re.sub(r"<p>\s*(?:<strong>)?\s*How to interpret the numbers[^<]*(?:</strong>)?.*?</p>", "",
                  html, flags=re.I | re.S)
    html = _EMPTY_BENCH.sub("<td>\u2014</td>", html)
    html = wrap_bare_paragraphs(html)

    soup = BeautifulSoup(html, "html.parser")
    _populate_reference_benchmarks(soup)
    _deduplicate_section_tables(soup)
    _enforce_staged_plan_and_quick_wins(soup)
    _enforce_country_deep_links(soup, cname, cc)
    return str(soup)


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
