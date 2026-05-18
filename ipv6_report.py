"""
ipv6_report.py
==============
CLI entry point for the IPv6 Policy Engine.
Run from the pulse-reporter root directory:

    python ipv6_report.py FR
    python ipv6_report.py MA --year 2023
    python ipv6_report.py KZ --no-export

Prints a formatted ASCII report to the terminal and auto-saves
a Markdown policy brief to reports/IPv6_<COUNTRY>_<DATE>.md
"""

import sys
import os
import pathlib
import argparse
from datetime import datetime

# ── Ensure root is on sys.path ───────────────────────────────────────────────
ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from request_for_YPI.ipv6_engine import (
    build_scorecard,
    generate_executive_summary,
    get_adoption_trend,
    get_regional_comparison,
    export_policy_brief,
)


# ═══════════════════════════════════════════════════════════════════════════
# TERMINAL FORMATTING HELPERS
# ═══════════════════════════════════════════════════════════════════════════

WIDTH = 72

def _hr(char="━"):
    return char * WIDTH

def _header(title):
    pad = (WIDTH - len(title) - 2) // 2
    return f"{'━' * pad} {title} {'━' * (WIDTH - pad - len(title) - 2)}"

def _line(label, value, width=28):
    return f"  {label:<{width}}{value}"

# Archetype colour codes (terminal ANSI — works on Windows 10+ with PowerShell)
_RESET  = "\033[0m"
_RED    = "\033[91m"
_YELLOW = "\033[93m"
_CYAN   = "\033[96m"
_GREEN  = "\033[92m"
_BOLD   = "\033[1m"

_ARCHETYPE_COLOUR = {
    "A":  _RED,
    "C":  _YELLOW,
    "D":  _RED + _BOLD,
    "OK": _GREEN,
}


def _coloured(text, colour):
    return f"{colour}{text}{_RESET}"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION PRINTERS
# ═══════════════════════════════════════════════════════════════════════════

def print_scorecard(scorecard: dict):
    isps  = scorecard.get("isps", [])
    stats = scorecard.get("summary", {})
    nat   = scorecard.get("national_adoption", 0)

    print(f"\n{_header('SECTION 2 — ISP COMPLIANCE SCORECARD')}")
    print()
    print(_line("National IPv6 Adoption:",  f"{nat*100:.1f}%"))
    print(_line("ISPs Assessed:",            str(stats.get("total_isps", 0))))
    print(_line("Ghost (Cat A):",            str(stats.get("ghost_count", 0))))
    print(_line("Laggard (Cat C):",          str(stats.get("laggard_count", 0))))
    print(_line("Bottleneck (Cat D):",       str(stats.get("bottleneck_count", 0))))
    print(_line("Compliant (OK):",           str(stats.get("compliant_count", 0))))
    print(_line("Underserved Market Share:", f"{stats.get('combined_underserved_pct', 0):.1f}%"))
    print()

    # Table header
    col = "{:<8} {:<32} {:>8} {:>9} {:>8} {:>11} {:>12} {:>14}"
    print(_BOLD + col.format(
        "ASN", "ISP", "Mkt Shr", "IPv6 PFX",
        "ConeSize", "Adoption", "Archetype", "Impact (pp)"
    ) + _RESET)
    print("─" * WIDTH)

    for isp in isps:
        arch   = isp["archetype"]
        colour = _ARCHETYPE_COLOUR.get(arch, "")
        label  = f"{arch} — {isp['archetype_label']}"

        row = col.format(
            f"AS{isp['asn']}",
            isp["isp"][:32],
            f"{isp['market_share_pct']:.1f}%",
            str(isp["ipv6_prefixes"]),
            str(isp["cone_size"]),
            f"{isp['ipv6_adoption_est']*100:.1f}%",
            arch,
            f"+{isp['projected_impact_pp']:.1f}",
        )
        print(_coloured(row, colour))

    print("─" * WIDTH)
    print()
    print("  Archetype Key:")
    print(_coloured("    A = Ghost (No Allocation)   → RIR mandate", _RED))
    print(_coloured("    C = Laggard (No Traffic)    → CPE/hardware standards", _YELLOW))
    print(_coloured("    D = Bottleneck (HIGH IMPACT) → Direct govt engagement", _RED + _BOLD))
    print(_coloured("    OK= Compliant", _GREEN))


def print_trend(trend: list, country: str):
    print(f"\n{_header('SECTION 3 — USER-SIDE ADOPTION TREND')}")
    print()
    print(_line("Country:", country))
    print()

    bar_max = 40
    prev    = None

    for t in trend:
        year = t["year"]
        val  = t["adoption"]

        if val is None:
            print(f"  {year}  {'No data':>8}  {'':40}")
            continue

        pct  = val * 100
        bars = int((pct / 100) * bar_max)
        bar  = "█" * bars + "░" * (bar_max - bars)

        if prev is not None:
            delta = val - prev
            chg   = f"  {delta*100:+.1f} pp"
        else:
            chg   = ""

        print(f"  {year}  {pct:>6.1f}%  {bar}{chg}")
        prev = val


def print_comparison(comparison: dict):
    if comparison.get("error"):
        print(f"\n  [Regional comparison unavailable: {comparison['error']}]")
        return

    ref   = comparison["reference"]
    g_avg = comparison["global_average_pct"]
    rank  = comparison["global_rank"]
    total = comparison["total_countries"]
    diff  = ref["adoption_pct"] - g_avg
    above = "ABOVE" if comparison["above_global_avg"] else "BELOW"

    print(f"\n{_header('SECTION 3 — REGIONAL POSITION')}")
    print()
    print(_line(f"{ref['country']} Adoption:",   f"{ref['adoption_pct']}%"))
    print(_line("Global Average:",               f"{g_avg}%"))
    print(_line("vs Global Average:",            f"{diff:+.1f} pp  [{above} average]"))
    print(_line("Global Rank:",                  f"#{rank} of {total} countries"))
    print()
    print("  Closest peer countries (by adoption score):")
    print()
    print(f"  {'Country':<10} {'Adoption':>10} {'Gap':>10}")
    print("  " + "─" * 32)
    for p in comparison.get("closest_peers", []):
        gap = p["adoption_pct"] - ref["adoption_pct"]
        print(f"  {p['country']:<10} {p['adoption_pct']:>9.1f}% {gap:>+9.1f} pp")


def print_executive_summary(text: str):
    print(f"\n{_header('EXECUTIVE SUMMARY')}")
    print()
    # Word-wrap at ~68 chars
    words   = text.split()
    line    = "  "
    for word in words:
        if len(line) + len(word) + 1 > 70:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="IPv6 Policy Engine — ISOC Pulse × IYP"
    )
    parser.add_argument(
        "country",
        type=str,
        help="ISO-2 country code (e.g. FR, MA, KZ)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2024,
        help="Data year for Pulse API (default: 2024)"
    )
    parser.add_argument(
        "--trend-start",
        type=int,
        default=2020,
        dest="trend_start",
        help="Start year for adoption trend (default: 2020)"
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        dest="no_export",
        help="Skip saving the Markdown policy brief"
    )
    args = parser.parse_args()

    country = args.country.upper()

    # ── Banner ───────────────────────────────────────────────────────────────
    print()
    print(_hr())
    print(_BOLD + f"  IPv6 POLICY ENGINE — COUNTRY REPORT: {country}" + _RESET)
    print(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Data Year : {args.year}")
    print(f"  Sources   : ISOC Pulse API · Internet Yellow Pages (IYP) Neo4j")
    print(f"  Framework : ISOC IRI — Security Pillar → Enabling Technologies → IPv6")
    print(_hr())

    # ── Section 2: Scorecard ─────────────────────────────────────────────────
    print(f"\n  [1/4] Building ISP scorecard for {country}...", end=" ", flush=True)
    scorecard = build_scorecard(country, year=args.year)

    if scorecard.get("error"):
        print(f"\n  [ERROR] {scorecard['error']}")
        sys.exit(1)

    print("done.")
    print_scorecard(scorecard)

    # ── Section 3: Trend ─────────────────────────────────────────────────────
    print(f"\n  [2/4] Fetching adoption trend ({args.trend_start}–{args.year})...",
          end=" ", flush=True)
    trend = get_adoption_trend(country, start_year=args.trend_start, end_year=args.year)
    print("done.")
    print_trend(trend, country)

    # ── Section 3: Regional comparison ───────────────────────────────────────
    print(f"\n  [3/4] Computing regional comparison...", end=" ", flush=True)
    comparison = get_regional_comparison(country, year=args.year)
    print("done.")
    print_comparison(comparison)

    # ── Executive Summary ─────────────────────────────────────────────────────
    print(f"\n  [4/4] Generating executive summary...", end=" ", flush=True)
    summary_text = generate_executive_summary(scorecard)
    print("done.")
    print_executive_summary(summary_text)

    # ── Export ────────────────────────────────────────────────────────────────
    if not args.no_export:
        print()
        filepath = export_policy_brief(
            scorecard    = scorecard,
            summary_text = summary_text,
            trend        = trend,
            comparison   = comparison,
        )
        print(_hr("─"))
        print(f"  [EXPORT] Policy brief saved →  {filepath}")
        print(_hr("─"))

    print()
    print(_hr())
    print()


if __name__ == "__main__":
    main()
