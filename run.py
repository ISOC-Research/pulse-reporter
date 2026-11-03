"""
run.py — Unified, simple CLI for ISOC Pulse Report Generation
=============================================================
Run `python run.py help` (or `python run.py` with no arguments) to see the full command guide.
"""

import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS = {"peering", "ipv6", "dnssec", "all"}

RAW_SCRIPTS = {
    "peering": "peering_report.py",
    "ipv6": "ipv6_report.py",
    "dnssec": "dnssec_report.py",
}

TITLE_MAP = {
    "peering": "Peering",
    "ipv6": "IPv6",
    "dnssec": "DNSSEC",
}

HELP_TEXT = """
================================================================================
  ISOC PULSE REPORTER — QUICK COMMAND GUIDE
================================================================================

  1. FULL PIPELINE (Fetches live .md data + Generates .html & .docx Word report)
  ------------------------------------------------------------------------------
  python run.py peering IN          Full Peering report for India (works on Student Wi-Fi)
  python run.py ipv6 IN             Full IPv6 report for India
  python run.py dnssec IN           Full DNSSEC report for India
  python run.py all IN              Run ALL 3 metrics (Peering, IPv6, DNSSEC) for India

  * Tip: Replace 'IN' with any 2-letter country code (FR, MA, SO, BR, US, DE...).
  * Tip: Argument order doesn't matter ('python run.py IN peering' also works).

  2. STEP-BY-STEP MODES (Optional Flags)
  ------------------------------------------------------------------------------
  python run.py peering IN --raw    STEP 1 ONLY: Fetch/update raw .md file only
                                    (Does not call Gemini LLM or build HTML/Word)

  python run.py peering IN --brief  STEP 2 ONLY: Build .html & .docx from saved .md
                                    (Skips live API queries; great for Student Wi-Fi!)
  python run.py ipv6 IN --brief     Rebuild IPv6 HTML & Word from cached .md
  python run.py dnssec IN --brief   Rebuild DNSSEC HTML & Word from cached .md

  3. STUDENT WI-FI NOTES (When IYP Port 7687 is Blocked)
  ------------------------------------------------------------------------------
  - Peering ('python run.py peering <CC>') works 100% end-to-end for ANY country.
  - IPv6 & DNSSEC automatically fall back to cached .md files (IN, FR, MA, SO)
    if live IYP queries fail, or use '--brief' to skip straight to HTML/Word.

  4. WHERE OUTPUT FILES ARE SAVED
  ------------------------------------------------------------------------------
  - Word Docs (.docx) : reports/<metric>/word/<Topic>_Report_<CC>.docx
  - Web Brief (.html) : reports/<metric>/html/<Topic>_Policy_Brief_<CC>.html
  - Raw Data  (.md)   : reports/<metric>/raw/<Topic>_Report_<CC>.md

  5. HELP
  ------------------------------------------------------------------------------
  python run.py help                Show this command guide
  python run.py --help              Show this command guide
================================================================================
"""


def run_metric(topic: str, country: str, raw_only: bool, brief_only: bool):
    title = TITLE_MAP[topic]
    md_path = os.path.join(HERE, "reports", topic, "raw", f"{title}_Report_{country}.md")

    # 1. Step 1: Fetch raw .md data (unless --brief was passed)
    if not brief_only:
        script = os.path.join(HERE, RAW_SCRIPTS[topic])
        print(f"\n{'='*64}")
        print(f"▶ STEP 1 [{title} — {country}]: Fetching live metrics -> .md")
        print(f"{'='*64}")
        res = subprocess.run([sys.executable, script, country], cwd=HERE)
        if res.returncode != 0:
            if os.path.exists(md_path) and not raw_only:
                print(f"\n⚠️ Live data fetch failed (e.g., IYP port 7687 blocked on Wi-Fi).")
                print(f"   Falling back to cached raw report: {md_path}")
            else:
                print(f"\n❌ Failed to fetch raw data for {title} ({country}) and no cached .md found.")
                return

    if raw_only:
        return

    # 2. Step 2: Generate HTML + Word (.docx) from the .md file
    print(f"\n{'='*64}")
    print(f"▶ STEP 2 [{title} — {country}]: Generating HTML Dashboard & Word (.docx)")
    print(f"{'='*64}")
    brief_script = os.path.join(HERE, "generate_llm_brief.py")
    subprocess.run([sys.executable, brief_script, topic, country], cwd=HERE)


def main():
    args = [a.strip() for a in sys.argv[1:]]
    if not args or any(a.lower() in {"help", "-h", "--help", "?"} for a in args):
        print(HELP_TEXT.strip("\n"))
        sys.exit(0)

    raw_only = False
    brief_only = False
    pos = []
    for a in args:
        al = a.lower()
        if al in {"--raw", "--md", "raw", "md"}:
            raw_only = True
        elif al in {"--brief", "--html", "--word", "brief", "html"}:
            brief_only = True
        elif not a.startswith("-"):
            pos.append(a)

    if len(pos) < 2:
        print("❌ Missing metric or country code.")
        print(HELP_TEXT.strip("\n"))
        sys.exit(1)

    a1, a2 = pos[0].lower(), pos[1].lower()
    if a1 in TOPICS:
        topic, country = a1, pos[1].upper()
    elif a2 in TOPICS:
        topic, country = a2, pos[0].upper()
    else:
        print(f"❌ Could not recognize metric '{pos[0]}'. Choose from: peering, ipv6, dnssec, all")
        print(HELP_TEXT.strip("\n"))
        sys.exit(1)

    metrics = ["peering", "ipv6", "dnssec"] if topic == "all" else [topic]
    for m in metrics:
        run_metric(m, country, raw_only=raw_only, brief_only=brief_only)


if __name__ == "__main__":
    main()
