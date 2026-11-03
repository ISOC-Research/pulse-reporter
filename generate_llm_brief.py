import argparse
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

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


def main():
    parser = argparse.ArgumentParser(description="Generate an LLM Policy Brief from a Report.")
    parser.add_argument("arg1", type=str, help="Topic (ipv6, dnssec, peering) or Country code (e.g., FR, IN)")
    parser.add_argument("arg2", type=str, nargs="?", default=None, help="Country code or Topic")
    parser.add_argument("--topic", "-t", type=str, default=None, help="Optional topic flag (ipv6, dnssec, peering)")
    args = parser.parse_args()

    topics = {"ipv6", "dnssec", "peering"}
    a1 = args.arg1.lower()
    a2 = args.arg2.lower() if args.arg2 else None
    t_flag = args.topic.lower() if args.topic else None

    if t_flag in topics:
        topic = t_flag
        country = args.arg1.upper()
    elif a1 in topics and a2:
        topic = a1
        country = args.arg2.upper()
    elif a2 in topics:
        topic = a2
        country = args.arg1.upper()
    else:
        print("❌ Usage: python generate_llm_brief.py <peering|ipv6|dnssec> <COUNTRY_CODE>")
        sys.exit(1)

    # Capitalize properly for filenames
    if topic == "ipv6":
        topic_title = "IPv6"
    elif topic == "dnssec":
        topic_title = "DNSSEC"
    elif topic == "peering":
        topic_title = "Peering"

    raw_dir = os.path.join("reports", topic, "raw")
    html_dir = os.path.join("reports", topic, "html")
    word_dir = os.path.join("reports", topic, "word")
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(word_dir, exist_ok=True)
    report_path = os.path.join(raw_dir, f"{topic_title}_Report_{country}.md")
    if not os.path.exists(report_path):
        legacy = os.path.join("reports", f"{topic_title}_Report_{country}.md")
        if os.path.exists(legacy):
            report_path = legacy
    output_path = os.path.join(html_dir, f"{topic_title}_Policy_Brief_{country}.html")

    if not os.path.exists(report_path):
        print(f"❌ ERROR: Could not find report file at {report_path}")
        print(f"   Please run `python run.py {topic} {country}` first to generate the data.")
        sys.exit(1)

    print(f"📄 Reading raw data from {report_path}...")
    with open(report_path, "r", encoding="utf-8") as f:
        report_data = f.read()

    from datetime import datetime
    from docx_builder import country_name, export_word_safe
    from html_theme import apply_isoc_theme, prepare_html_content
    from isoc_report import build_isoc_system_prompt, build_isoc_user_prompt, generate_isoc_content, postprocess_isoc_html

    cname = country_name(country)
    system_instruction = build_isoc_system_prompt(topic_title, cname, country)

    try:
        prompt = build_isoc_user_prompt(topic_title, cname, country, report_data)
        llm_html = generate_isoc_content(genai, system_instruction, prompt)

        html_template = HTML_TEMPLATE.replace("IPv6 Policy Brief", f"{topic_title} Policy Brief")
        html_template = html_template.replace("IPv6 Readiness", f"{topic_title} Readiness")
        html_template = html_template.replace("IPv6 Policy Engine", f"{topic_title} Policy Engine")

        docx_name = f"{topic_title}_Report_{country}.docx"
        html_template = apply_isoc_theme(
            html_template, topic_title, f"../word/{docx_name}", country,
            sources={
                "ipv6": "Data Sources: ISOC Pulse API · Internet Yellow Pages (IYP)",
                "dnssec": "Data Sources: Internet Yellow Pages (IYP) · Cloudflare Radar",
                "peering": "Data Sources: PeeringDB · PCH · RIPEstat · ISOC Pulse",
            }[topic],
        )

        llm_html = postprocess_isoc_html(llm_html, cname, country)
        web_content = prepare_html_content(llm_html)

        final_html = html_template.format(
            country=country,
            date=datetime.now().strftime("%B %Y"),
            llm_content=web_content
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)

        print(f"✅ Success! Policy Brief saved to: {output_path}")
        print(f"   Open it in Chrome and press Ctrl+P to save as PDF.")

        export_word_safe(llm_html, topic_title, country,
                         os.path.join(word_dir, docx_name))

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
