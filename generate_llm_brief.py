import argparse
import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv

# Ensure stdout supports UTF-8 for emojis on Windows
if sys.stdout.encoding.lower() != 'utf-8':
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
    <title>IPv6 Policy Brief — {country}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad: true, theme: 'default', themeVariables: {{ 'pie1': '#1e88e5', 'pie2': '#43a047', 'pie3': '#fb8c00', 'pie4': '#e53935', 'pie5': '#8e24aa', 'pie6': '#00acc1', 'pie7': '#f4511e', 'pie8': '#3949ab', 'pie9': '#7cb342', 'pie10': '#c0ca33', 'pie11': '#039be5', 'pie12': '#d81b60', 'xyChart': {{ 'backgroundColor': '#ffffff', 'titleColor': '#1a237e', 'xAxisLabelColor': '#333333', 'yAxisLabelColor': '#333333', 'plotColorPalette': '#1e88e5, #43a047, #fb8c00, #e53935, #8e24aa' }} }} }});</script>
    <style>
        :root {{
            --primary: #1a237e;
            --primary-light: #3949ab;
            --accent: #00bcd4;
            --accent-warm: #ff6f00;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #212529;
            --text-muted: #6c757d;
            --border: #e9ecef;
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
            background: linear-gradient(135deg, #0d1b3e 0%, #1a237e 40%, #283593 70%, #3949ab 100%);
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
            background: radial-gradient(ellipse, rgba(0, 188, 212, 0.12) 0%, transparent 70%);
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
        tbody tr:nth-child(even) {{ background: #f8f9ff; }}
        tbody tr:hover {{ background: #eef0ff; }}

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
            background: #e8eaf6;
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
            background: linear-gradient(135deg, #1a237e, #283593);
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

        strong {{ color: #1a237e; }}
    </style>
</head>
<body>

<!-- ═══ COVER PAGE ═══ -->
<div class="cover">
    <div class="cover-badge">Internet Society · Pulse Platform</div>
    <div class="cover-country">{country}</div>
    <div class="cover-title">IPv6 Readiness & Policy Brief</div>
    <div class="cover-line"></div>
    <div class="cover-meta">
        Generated: {date}<br>
        Data Sources: ISOC Pulse API · Internet Yellow Pages (IYP) Neo4j<br>
        Framework: ISOC Internet Resilience Index — Security Pillar
    </div>
</div>

<!-- ═══ REPORT BODY (LLM-generated) ═══ -->
<div class="content">
{llm_content}

    <div class="footer">
        <p>Report generated by ISOC Pulse × IYP IPv6 Policy Engine</p>
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
    Load the French team's synthesis prompt if available,
    then add our strict HTML-output rules.
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

You MUST output raw HTML content (NOT markdown). Your output will be injected directly into an HTML page.
Follow these rules strictly:

### ADDRESSING RULES (CRITICAL)
- Do NOT address the reader as "Mr. President", "Prime Minister", "Your Excellency", or any specific title.
- If you need to address the reader, use "Sir/Ma'am" or simply say "Decision-Makers".
- Write in a professional but neutral tone suitable for any senior government or regulatory official.
- NOTE: Audience-specific formatting tiers (Head of State, Minister, Regulator, Technical) will be added in a future version.

### Text & Structure
- Use <h1> for major section titles (e.g., "Executive Summary", "SWOT Analysis", "Strategic Roadmap").
- Use <h2> for subsections.
- Use <h3> for minor headings.
- Use <p> for paragraphs. Wrap key facts in <strong> tags.
- Use <ul>/<ol> and <li> for lists.

### Stat Cards
For key metrics, output this exact HTML structure:
<div class="stat-grid">
  <div class="stat-card"><span class="number">86.9%</span><span class="label">National IPv6 Adoption</span></div>
  <div class="stat-card"><span class="number">#3</span><span class="label">Global Ranking</span></div>
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
Wrap mermaid charts inside a container. The page uses a vibrant Mermaid color palette — charts will render with rich blues, greens, oranges, and reds automatically.
<div class="chart-container">
  <h3>Chart Title</h3>
  <div class="mermaid">
pie title ISP Market Share
    "Orange" : 35.4
    "Free SAS" : 18.6
  </div>
</div>

Include at LEAST:
1. A Pie Chart for ISP Market Share (use the top 5-8 ISPs for readability — do NOT include every single ISP).
2. A Bar Chart (xychart-beta) for the 5-Year Adoption Trend. You MUST use xychart-beta syntax, NEVER use "lineChart". Example:
<div class="mermaid">
xychart-beta
    title "National IPv6 Adoption Trend"
    x-axis [2020, 2021, 2022, 2023, 2024]
    y-axis "Adoption (%)" 0 --> 100
    bar [67.7, 71.9, 89.1, 87.0, 86.9]
</div>
3. A Pie Chart or Bar Chart for Sector IPv6 Readiness (Banking, News, Education, Ecommerce).
4. A Bar Chart comparing Web IPv6 Readiness across categories (Government, CDN-backed, Self-hosted, etc.) if the data is available.

### Final Verdict
<div class="verdict">
  <h2>Final Verdict</h2>
  <p>Summary paragraph.</p>
  <div class="verdict-scores">
    <div class="verdict-item"><div class="score">High</div><div class="score-label">Investability</div></div>
    <div class="verdict-item"><div class="score">Developing</div><div class="score-label">Maturity</div></div>
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
    parser = argparse.ArgumentParser(description="Generate an LLM Policy Brief from an IPv6 Report.")
    parser.add_argument("country", type=str, help="Country code (e.g., FR, IN)")
    args = parser.parse_args()

    country = args.country.upper()
    report_path = os.path.join("reports", f"IPv6_Report_{country}.md")
    output_path = os.path.join("reports", f"IPv6_Policy_Brief_{country}.html")

    if not os.path.exists(report_path):
        print(f"❌ ERROR: Could not find report file at {report_path}")
        print(f"   Please run `python ipv6_report.py {country}` first to generate the data.")
        sys.exit(1)

    print(f"📄 Reading raw data from {report_path}...")
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
            f"Here is the complete raw IPv6 data report for country code {country}. "
            f"Generate the Executive Policy Brief as raw HTML following your system instructions.\n\n"
            f"{report_data}"
        )

        response = model.generate_content(prompt)
        llm_html = response.text

        # Clean up in case the LLM wraps it in code fences anyway
        llm_html = llm_html.removeprefix("```html")
        llm_html = llm_html.removeprefix("```")
        llm_html = llm_html.removesuffix("```")
        llm_html = llm_html.strip()

        # Convert any leftover markdown **bold** to <strong> tags
        import re
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
                    # Remove parentheses content to save space (e.g. ASNs, "(Overall)")
                    clean_x = re.sub(r'\s*\(.*?\)', '', clean_x)
                    # Truncate if still too long
                    if len(clean_x) > 15:
                        clean_x = clean_x[:13] + '..'
                    quoted.append(f'"{clean_x}"')
                return prefix + '[' + ', '.join(quoted) + ']'
            return re.sub(r'(x-axis.*?)(?:\[(.*?)\])', quote_xaxis, block)
        llm_html = re.sub(r'xychart-beta.*?(?:</div>|</pre>)', fix_xychart, llm_html, flags=re.DOTALL)

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

        print(f"✅ Success! Policy Brief saved to: {output_path}")
        print(f"   Open it in Chrome and press Ctrl+P to save as PDF.")

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
