"""
generate_dnssec_brief.py
========================

Generates a styled HTML Policy Brief from DNSSEC raw report data
using Google Gemini. Mirrors the IPv6 brief generator architecture.

Usage:
    python generate_dnssec_brief.py FR

Prerequisites:
    1. Run `python dnssec_report.py FR` first to generate the raw data.
    2. Set REPORT_GEN_KEY in your .env file (Google Gemini API key).

Future: This will be merged into a unified report generator with
dropdown-based story selection (IPv6 / DNSSEC / combined) and
audience-tier formatting (Head of State / Minister / Regulator / Technical).
"""

import argparse
import os
import re
import sys

import google.generativeai as genai
from dotenv import load_dotenv

# Ensure stdout supports UTF-8 for emojis on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

api_key = os.getenv("REPORT_GEN_KEY")
if not api_key:
    print("❌ ERROR: REPORT_GEN_KEY not found in .env file.")
    sys.exit(1)

genai.configure(api_key=api_key)


# ═══════════════════════════════════════════════════════════════
# HTML TEMPLATE — The visual wrapper for the LLM content
# ═══════════════════════════════════════════════════════════════

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNSSEC Policy Brief — {country}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad: true, theme: 'default', themeVariables: {{ 'pie1': '#43a047', 'pie2': '#e53935', 'pie3': '#fb8c00', 'pie4': '#b71c1c', 'pie5': '#1e88e5', 'pie6': '#8e24aa', 'pie7': '#00acc1', 'pie8': '#f4511e', 'pie9': '#3949ab', 'pie10': '#7cb342', 'pie11': '#039be5', 'pie12': '#d81b60', 'xyChart': {{ 'backgroundColor': '#ffffff', 'titleColor': '#0d47a1', 'xAxisLabelColor': '#333333', 'yAxisLabelColor': '#333333', 'plotColorPalette': '#43a047, #e53935, #fb8c00, #1e88e5, #8e24aa' }} }} }});</script>
    <style>
        :root {{
            --primary: #0d47a1;
            --primary-light: #1565c0;
            --accent: #00e676;
            --accent-warm: #ff6f00;
            --bg: #f5f7fa;
            --card-bg: #ffffff;
            --text: #212529;
            --text-muted: #6c757d;
            --border: #e0e4ea;
            --green: #2e7d32;
            --red: #c62828;
            --yellow: #f57f17;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            font-size: 15px;
        }}

        /* ── COVER PAGE ── */
        .cover {{
            min-height: 100vh;
            background: linear-gradient(135deg, #0a1628 0%, #0d47a1 35%, #1565c0 65%, #1976d2 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            padding: 60px 40px;
            position: relative;
            overflow: hidden;
            page-break-after: always;
        }}
        .cover::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -30%;
            width: 80%;
            height: 200%;
            background: radial-gradient(ellipse, rgba(0, 230, 118, 0.1) 0%, transparent 70%);
            pointer-events: none;
        }}
        .cover-badge {{
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 50px;
            padding: 8px 24px;
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
        }}
        .cover-country {{
            font-size: 96px;
            font-weight: 800;
            letter-spacing: 8px;
            margin-bottom: 16px;
            text-shadow: 0 4px 30px rgba(0,0,0,0.3);
        }}
        .cover-title {{
            font-size: 28px;
            font-weight: 300;
            opacity: 0.9;
            margin-bottom: 60px;
            max-width: 600px;
        }}
        .cover-meta {{
            font-size: 13px;
            opacity: 0.6;
            line-height: 2;
        }}
        .cover-line {{
            width: 80px;
            height: 3px;
            background: var(--accent);
            margin: 30px auto;
            border-radius: 2px;
        }}

        /* ── MAIN CONTENT ── */
        .content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 40px;
        }}

        /* ── SECTION HEADERS ── */
        h1 {{
            font-size: 32px;
            font-weight: 800;
            color: var(--primary);
            margin: 50px 0 24px 0;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--accent);
            page-break-before: always;
        }}
        h1:first-child {{ page-break-before: avoid; }}

        h2 {{
            font-size: 22px;
            font-weight: 700;
            color: var(--primary-light);
            margin: 40px 0 16px 0;
            padding-left: 16px;
            border-left: 4px solid var(--accent);
        }}

        h3 {{
            font-size: 17px;
            font-weight: 600;
            color: var(--text);
            margin: 28px 0 12px 0;
        }}

        p {{
            margin-bottom: 16px;
            color: #333;
        }}

        /* ── STAT CARDS ── */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }}
        .stat-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid var(--border);
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: 800;
            color: var(--primary);
            display: block;
        }}
        .stat-card .label {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}

        /* ── TABLES ── */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            border-radius: 10px;
            overflow: hidden;
        }}
        thead th {{
            background: var(--primary);
            color: white;
            padding: 14px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        tbody td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
        }}
        tbody tr:nth-child(even) {{ background: #f0f4ff; }}
        tbody tr:hover {{ background: #e3eaff; }}

        /* ── SWOT GRID ── */
        .swot-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 24px 0;
        }}
        .swot-card {{
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border);
        }}
        .swot-card h3 {{
            margin: 0 0 12px 0;
            font-size: 16px;
            border: none;
            padding: 0;
        }}
        .swot-card ul {{ padding-left: 20px; }}
        .swot-card li {{ margin-bottom: 8px; font-size: 14px; }}
        .swot-strengths {{ background: #e8f5e9; border-color: #a5d6a7; }}
        .swot-strengths h3 {{ color: var(--green); }}
        .swot-weaknesses {{ background: #fce4ec; border-color: #ef9a9a; }}
        .swot-weaknesses h3 {{ color: var(--red); }}
        .swot-opportunities {{ background: #e3f2fd; border-color: #90caf9; }}
        .swot-opportunities h3 {{ color: #1565c0; }}
        .swot-threats {{ background: #fff3e0; border-color: #ffcc80; }}
        .swot-threats h3 {{ color: var(--accent-warm); }}

        /* ── CALLOUT BOXES ── */
        .callout {{
            background: #e3f2fd;
            border-left: 4px solid var(--primary);
            border-radius: 0 10px 10px 0;
            padding: 20px 24px;
            margin: 20px 0;
            font-size: 14px;
        }}
        .callout-warning {{
            background: #fff3e0;
            border-left-color: var(--accent-warm);
        }}
        .callout-success {{
            background: #e8f5e9;
            border-left-color: var(--green);
        }}

        /* ── VERDICT BOX ── */
        .verdict {{
            background: linear-gradient(135deg, #0d47a1, #1565c0);
            color: white;
            border-radius: 16px;
            padding: 40px;
            margin: 40px 0;
            text-align: center;
        }}
        .verdict h2 {{
            color: white;
            border: none;
            padding: 0;
            margin: 0 0 24px 0;
            font-size: 24px;
        }}
        .verdict-scores {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 24px;
        }}
        .verdict-item .score {{
            font-size: 28px;
            font-weight: 800;
            color: var(--accent);
        }}
        .verdict-item .score-label {{
            font-size: 13px;
            opacity: 0.7;
            margin-top: 4px;
        }}
        .verdict p, .verdict li {{
            color: rgba(255, 255, 255, 0.92);
        }}
        .verdict strong {{
            color: #ffffff;
        }}

        /* ── MERMAID CHARTS ── */
        .chart-container {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 30px;
            margin: 24px 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid var(--border);
            text-align: center;
        }}
        .chart-container h3 {{
            margin: 0 0 20px 0;
            text-align: center;
        }}
        .mermaid {{ margin: 0 auto; }}

        /* ── PHASE CARDS ── */
        .phase {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 28px;
            margin: 16px 0;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .phase-badge {{
            display: inline-block;
            background: var(--primary);
            color: white;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 14px;
            border-radius: 20px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .phase-badge.medium {{ background: var(--primary-light); }}
        .phase-badge.long {{ background: #455a64; }}
        .phase ol {{ padding-left: 20px; }}
        .phase li {{ margin-bottom: 10px; font-size: 14px; }}

        /* ── LISTS ── */
        ul, ol {{ padding-left: 24px; margin-bottom: 16px; }}
        li {{ margin-bottom: 8px; }}

        /* ── FOOTER ── */
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 12px;
            border-top: 1px solid var(--border);
            margin-top: 60px;
        }}

        /* ── PRINT ── */
        @media print {{
            body {{ background: white; font-size: 13px; }}
            .cover {{ min-height: 100vh; }}
            .content {{ padding: 40px 30px; }}
            h1 {{ page-break-before: always; font-size: 26px; }}
            h1:first-child {{ page-break-before: avoid; }}
            .stat-card, .phase, .chart-container {{ break-inside: avoid; }}
            table {{ break-inside: avoid; }}
            .swot-grid {{ break-inside: avoid; }}
        }}

        strong {{ color: #0d47a1; }}
    </style>
</head>
<body>

<!-- ═══ COVER PAGE ═══ -->
<div class="cover">
    <div class="cover-badge">Internet Society · Pulse Platform</div>
    <div class="cover-country">{country}</div>
    <div class="cover-title">DNSSEC Readiness & Policy Brief</div>
    <div class="cover-line"></div>
    <div class="cover-meta">
        Generated: {date}<br>
        Data Sources: Internet Yellow Pages (IYP) Neo4j · Cloudflare Radar<br>
        Framework: ISOC Internet Resilience Index — Security Pillar (DNS Security)
    </div>
</div>

<!-- ═══ REPORT BODY (LLM-generated) ═══ -->
<div class="content">
{llm_content}

    <div class="footer">
        <p>Report generated by ISOC Pulse × IYP DNSSEC Policy Engine</p>
        <p>Team: Rahul Rajesh, Ron Prajoth, Aditya Menon | Mentor: Amreesh Phokeer (ISOC)</p>
    </div>
</div>

</body>
</html>
"""


# ═══════════════════════════════════════════════════════════════
# SYSTEM PROMPT — Instructions for the LLM
# ═══════════════════════════════════════════════════════════════

def build_system_prompt():
    """
    Build the system prompt for DNSSEC policy brief generation.
    Uses the same synthesis prompt as IPv6 if available,
    then adds DNSSEC-specific HTML output rules.
    """
    prompt_dir = os.path.join("request_for_YPI", "prompt", "report_generation")
    synthesis_path = os.path.join(prompt_dir, "part_7_synthesis.md")

    if os.path.exists(synthesis_path):
        with open(synthesis_path, "r", encoding="utf-8") as f:
            base_prompt = f.read()
    else:
        base_prompt = "You are a Chief Strategy Officer advising a senior government official on Telecommunications and Internet Policy."

    html_rules = """

## OUTPUT FORMAT (CRITICAL — READ CAREFULLY)

You are generating a DNSSEC (DNS Security Extensions) Policy Brief.
You MUST output raw HTML content (NOT markdown). Your output will be injected directly into an HTML page.
Follow these rules strictly:

### ADDRESSING RULES (CRITICAL)
- Do NOT address the reader as "Mr. President", "Prime Minister", "Your Excellency", or any specific title.
- If you need to address the reader, use "Sir/Ma'am" or simply say "Decision-Makers".
- Write in a professional but neutral tone suitable for any senior government or regulatory official.

### DNSSEC CONTEXT
DNSSEC is the security extension for the Domain Name System. It ensures that DNS responses
are authenticated and have not been tampered with. The report covers:
- Core Infrastructure: ccTLD nameserver count, IPv6 enablement, and ASN diversity
- DNSSEC Validation: What percentage of DNS queries are cryptographically validated
- Per-ASN Validation: Which ISPs/networks are validating DNSSEC and which are not

### Text & Structure
- Use <h1> for major section titles (e.g., "Executive Summary", "SWOT Analysis", "Strategic Roadmap").
- Use <h2> for subsections.
- Use <h3> for minor headings.
- Use <p> for paragraphs. Wrap key facts in <strong> tags.
- Use <ul>/<ol> and <li> for lists.

### Stat Cards
For key metrics, output this exact HTML structure:
<div class="stat-grid">
  <div class="stat-card"><span class="number">7</span><span class="label">Authoritative Nameservers</span></div>
  <div class="stat-card"><span class="number">85.7%</span><span class="label">IPv6 Enabled</span></div>
  <div class="stat-card"><span class="number">62.4%</span><span class="label">DNSSEC Secure Queries</span></div>
</div>

### Tables
Use standard <table>, <thead>, <tbody>, <tr>, <th>, <td> tags.

### SWOT Analysis
You MUST output the SWOT in this exact structure:
<div class="swot-grid">
  <div class="swot-card swot-strengths"><h3>💪 Strengths</h3><ul><li>...</li></ul></div>
  <div class="swot-card swot-weaknesses"><h3>⚠️ Weaknesses</h3><ul><li>...</li></ul></div>
  <div class="swot-card swot-opportunities"><h3>🚀 Opportunities</h3><ul><li>...</li></ul></div>
  <div class="swot-card swot-threats"><h3>🛡️ Threats</h3><ul><li>...</li></ul></div>
</div>

### Callout Boxes
For important warnings or highlights:
<div class="callout">Key insight here.</div>
<div class="callout callout-warning">Warning text here.</div>
<div class="callout callout-success">Positive highlight here.</div>

### Policy Roadmap Phases
<div class="phase"><span class="phase-badge">Phase 1 — Quick Wins</span><ol><li>...</li></ol></div>
<div class="phase"><span class="phase-badge medium">Phase 2 — Structural</span><ol><li>...</li></ol></div>
<div class="phase"><span class="phase-badge long">Phase 3 — Vision</span><ol><li>...</li></ol></div>

### Charts (Mermaid) — MUST BE COLORFUL
Wrap mermaid charts inside a container. The page uses a SEMANTIC color palette for DNSSEC:
- 1st entry (green) = Secure
- 2nd entry (red) = Insecure
- 3rd entry (amber) = Other
- 4th entry (dark red) = Invalid

You MUST always list pie chart entries in this exact order: Secure FIRST, then Insecure, then Other, then Invalid.
<div class="chart-container">
  <h3>Chart Title</h3>
  <div class="mermaid">
pie title DNSSEC Validation Status
    "Secure" : 9.0
    "Insecure" : 78.0
    "Other" : 13.5
    "Invalid" : 0.1
  </div>
</div>

Include at LEAST:
1. A Pie Chart for DNSSEC Validation Status. CRITICAL: Always list "Secure" FIRST so it renders in green, then "Insecure" in red, then "Other" in amber, then "Invalid" in dark red.
2. A Bar Chart (xychart-beta) comparing DNSSEC Secure Validation rates across the top ISPs/ASNs. You MUST use xychart-beta syntax, NEVER use "lineChart". Example:
<div class="mermaid">
xychart-beta
    title "DNSSEC Validation by Top Networks"
    x-axis ["ISP A", "ISP B", "ISP C", "ISP D"]
    y-axis "Secure Validation (%)" 0 --> 100
    bar [85.2, 62.4, 45.1, 30.0]
</div>
3. A Pie Chart showing DNS Query Share distribution among top ASNs.

### Final Verdict
<div class="verdict">
  <h2>Final Verdict</h2>
  <p>Summary paragraph about overall DNSSEC posture.</p>
  <div class="verdict-scores">
    <div class="verdict-item"><div class="score">Medium</div><div class="score-label">DNSSEC Maturity</div></div>
    <div class="verdict-item"><div class="score">Developing</div><div class="score-label">Infrastructure Resilience</div></div>
  </div>
</div>

### ABSOLUTE RULES
- Do NOT wrap your output in ```html or ``` code fences.
- Do NOT output any markdown. Only raw HTML.
- Do NOT invent or hallucinate any data. Use ONLY the numbers from the attached report.
- Do NOT address the reader as "Mr. President" or "Prime Minister" or any specific title. Use "Sir/Ma'am" if needed.
- The report must be readable by a non-technical policymaker in under 5 minutes.
"""
    return base_prompt + html_rules


def main():
    parser = argparse.ArgumentParser(description="Generate an LLM Policy Brief from a DNSSEC Report.")
    parser.add_argument("country", type=str, help="Country code (e.g., FR, IN)")
    args = parser.parse_args()

    country = args.country.upper()
    report_path = os.path.join("reports", f"DNSSEC_Report_{country}.md")
    output_path = os.path.join("reports", f"DNSSEC_Policy_Brief_{country}.html")

    if not os.path.exists(report_path):
        print(f"❌ ERROR: Could not find report file at {report_path}")
        print(f"   Please run `python dnssec_report.py {country}` first to generate the data.")
        sys.exit(1)

    print(f"📄 Reading raw DNSSEC data from {report_path}...")
    with open(report_path, "r", encoding="utf-8") as f:
        report_data = f.read()

    system_instruction = build_system_prompt()

    print("🤖 Sending data to Gemini 2.5 Flash...")

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        prompt = (
            f"Here is the complete raw DNSSEC data report for country code {country}. "
            f"Generate the DNSSEC Executive Policy Brief as raw HTML following your system instructions.\n\n"
            f"{report_data}"
        )

        response = model.generate_content(prompt)
        llm_html = response.text

        # Clean up in case the LLM wraps it in code fences anyway
        if llm_html.startswith("```html"):
            llm_html = llm_html[7:]
        if llm_html.startswith("```"):
            llm_html = llm_html[3:]
        if llm_html.endswith("```"):
            llm_html = llm_html[:-3]
        llm_html = llm_html.strip()

        llm_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', llm_html)

        # Fix xychart-beta x-axis labels with unquoted spaces/parentheses
        def fix_xychart(match):
            block = match.group(0)
            def quote_xaxis(m):
                prefix = m.group(1)
                items = [x.strip() for x in m.group(2).split(',')]
                quoted = []
                for x in items:
                    clean_x = x.strip('"\'')
                    clean_x = re.sub(r'\s*\(.*?\)', '', clean_x)
                    if len(clean_x) > 15:
                        clean_x = clean_x[:13] + '..'
                    quoted.append(f'"{clean_x}"')
                return prefix + '[' + ', '.join(quoted) + ']'
            return re.sub(r'(x-axis.*?)(?:\[(.*?)\])', quote_xaxis, block)
        llm_html = re.sub(r'xychart-beta.*?(?:</div>|</pre>)', fix_xychart, llm_html, flags=re.DOTALL)

        # Force pie chart ordering to match semantic colors
        def reorder_pie(match):
            block = match.group(0)
            lines = block.split('\n')
            new_lines = []
            entries = {}
            for line in lines:
                if '"Secure"' in line: entries['Secure'] = line
                elif '"Insecure"' in line: entries['Insecure'] = line
                elif '"Other"' in line: entries['Other'] = line
                elif '"Invalid"' in line: entries['Invalid'] = line
                else: new_lines.append(line)
            
            # Insert in precise order before the closing </div>
            insert_idx = len(new_lines) - 1 # before </div>
            if 'Invalid' in entries: new_lines.insert(insert_idx, entries['Invalid'])
            if 'Other' in entries: new_lines.insert(insert_idx, entries['Other'])
            if 'Insecure' in entries: new_lines.insert(insert_idx, entries['Insecure'])
            if 'Secure' in entries: new_lines.insert(insert_idx, entries['Secure'])
            
            return '\n'.join(new_lines)
            
        llm_html = re.sub(r'pie title DNSSEC Validation Status.*?</div>', reorder_pie, llm_html, flags=re.DOTALL)

        # Fix pie charts rendering a leftover 0% slice when sum != 100
        def fix_pie_sum(match):
            block = match.group(0)
            lines = block.split('\n')
            parsed = []
            total = 0.0
            lines_to_keep = []
            
            for i, line in enumerate(lines):
                m = re.search(r'(".*?")\s*:\s*([\d\.]+)', line)
                if m:
                    val = float(m.group(2))
                    if val < 0.5:
                        continue
                    parsed.append((len(lines_to_keep), val, line, m.group(1)))
                    total += val
                    lines_to_keep.append(line)
                else:
                    lines_to_keep.append(line)
                    
            if parsed and abs(total - 100.0) > 0.001 and total > 0:
                largest_idx = max(range(len(parsed)), key=lambda x: parsed[x][1])
                idx_in_lines, val, orig_line, orig_label = parsed[largest_idx]
                diff = 100.0 - total
                new_val = round(val + diff, 2)
                parsed[largest_idx] = (idx_in_lines, new_val, orig_line, orig_label)
                lines_to_keep[idx_in_lines] = re.sub(r'[\d\.]+\s*$', str(new_val), orig_line)
                
            for idx_in_lines, val, orig_line, orig_label in parsed:
                clean_label = re.sub(r'\s*\([\d\.]+\s*%?\)', '', orig_label.strip('"'))
                new_label = f'"{clean_label} ({val:g}%)"'
                lines_to_keep[idx_in_lines] = re.sub(r'".*?"', new_label, lines_to_keep[idx_in_lines], count=1)
                
            return '\n'.join(lines_to_keep)
        llm_html = re.sub(r'pie title.*?(?:</div>|</pre>)', fix_pie_sum, llm_html, flags=re.DOTALL)

        # Build final HTML
        from datetime import datetime
        final_html = HTML_TEMPLATE.format(
            country=country,
            date=datetime.now().strftime("%Y-%m-%d"),
            llm_content=llm_html
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)

        print(f"✅ Success! DNSSEC Policy Brief saved to: {output_path}")
        print(f"   Open it in Chrome and press Ctrl+P to save as PDF.")

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
