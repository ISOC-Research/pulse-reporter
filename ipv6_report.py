"""
ipv6_report.py
==============
CLI entry point for the IPv6 Policy Engine.
Run from the pulse-reporter root directory:

    python ipv6_report.py FR
    python ipv6_report.py MA --year 2023
    python ipv6_report.py KZ --no-export

Prints a formatted ASCII report to the terminal and auto-saves
a Markdown policy brief to reports/IPv6_Report_<COUNTRY>.md
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

# ── Suppress Langfuse logging warnings ───────────────────────────────────────
import logging
logging.getLogger("langfuse").setLevel(logging.CRITICAL)

from request_for_YPI.ipv6_engine import (
    build_scorecard,
    generate_executive_summary,
    get_adoption_trend,
    get_isp_rpki_coverage,
    get_regional_comparison,
    export_policy_brief,
    get_rpki_coverage,
    get_ipv6_upstream_connectivity,
    get_ixp_ipv6_peering,
    get_ipv6_deployment_age,
    get_sector_ipv6_readiness,
    get_tld_ipv6_health,
    get_tld_ipv6_trend,
    compare_tld_ipv6_readiness,
    get_nameserver_ipv6_health,
    get_glue_record_ipv6_health,
    get_web_ipv6_readiness,
    get_government_ipv6_readiness,
    get_cdn_ipv6_correlation,
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
_DIM    = "\033[2m"

_ARCHETYPE_COLOUR = {
    "A":  _RED,
    "C":  _YELLOW,
    "D":  _RED + _BOLD,
    "OK": _GREEN,
}


def _coloured(text, colour):
    return f"{colour}{text}{_RESET}"


def _progress_bar(pct, width=30):
    """Return a coloured progress bar for a percentage value (0-100)."""
    filled = int((pct / 100) * width)
    bar = "█" * filled + "░" * (width - filled)

    if pct >= 75:
        colour = _GREEN
    elif pct >= 40:
        colour = _YELLOW
    else:
        colour = _RED

    return f"{colour}{bar}{_RESET} {pct:.1f}%"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION PRINTERS
# ═══════════════════════════════════════════════════════════════════════════

# ── Section 1: Core Infrastructure ───────────────────────────────────────

def print_rpki(rpki_data: dict):
    print(f"\n{_header('SECTION 1.1 — RPKI ROUTING SECURITY')}")
    print()

    total = rpki_data.get("total_ipv6_prefixes", 0)
    covered = rpki_data.get("rpki_covered_prefixes", 0)
    pct = rpki_data.get("coverage_pct", 0)

    print(_line("IPv6 Prefixes Announced:", f"{total:,}"))
    print(_line("RPKI-Covered Prefixes:",   f"{covered:,}"))
    print(_line("RPKI Coverage:",           _progress_bar(pct)))
    print()


def print_isp_rpki(isp_rpki_data: dict):
    isps = isp_rpki_data.get("isps", [])
    if not isps:
        return

    weakest = sorted(isps, key=lambda x: x["coverage_pct"])[:5]

    print(f"\n{_header('SECTION 1.1.3 — WEAKEST RPKI COVERAGE ISPs')}")
    print()

    col = "{:<8} {:<32} {:>12} {:>14}"
    print(_BOLD + col.format("ASN", "ISP", "IPv6 PFX", "RPKI Cov.") + _RESET)
    print("─" * WIDTH)

    for isp in weakest:
        pct = isp["coverage_pct"]
        colour = _RED if pct < 50 else (_YELLOW if pct < 80 else _GREEN)
        row = col.format(
            f"AS{isp.get('asn', '?')}",
            isp["isp"][:32],
            str(isp["total_ipv6_prefixes"]),
            f"{pct:.1f}%",
        )
        print(_coloured(row, colour))

    print("─" * WIDTH)
    print()


def print_upstream(upstream_data: dict):
    print(f"\n{_header('SECTION 1.2 — IPv6 UPSTREAM CONNECTIVITY')}")
    print()

    total = upstream_data.get("total_isps", 0)
    pct = upstream_data.get("percentage", 0)

    print(_line("ISPs Assessed:",              str(total)))
    print(_line("IPv6-Capable Upstream:",       _progress_bar(pct)))
    print()
    print(_DIM + "  ⚠ Experimental metric — based on inferred AS dependency relationships." + _RESET)
    print()


def print_ixp_peering(ixp_data: dict):
    print(f"\n{_header('SECTION 1.2.2 — IXP IPv6 PEERING')}")
    print()

    total_ixps = ixp_data.get("total_ixps", 0)
    ipv6_ixps = ixp_data.get("ipv6_capable_ixps", 0)
    ixp_pct = ixp_data.get("ixp_ipv6_pct", 0)
    member_pct = ixp_data.get("member_ipv6_pct", 0)

    print(_line("Domestic IXPs:",               str(total_ixps)))
    print(_line("IXPs with IPv6 LAN:",          f"{ipv6_ixps}  ({ixp_pct}%)"))
    print(_line("IXP IPv6 Readiness:",          _progress_bar(ixp_pct)))
    print()
    print(_line("Total IXP Members:",           str(ixp_data.get("total_members", 0))))
    print(_line("Members with IPv6 Peering:",   str(ixp_data.get("ipv6_members", 0))))
    print(_line("Member IPv6 Peering Rate:",    _progress_bar(member_pct)))
    print()

    # Top IXPs table
    ixps = ixp_data.get("ixps", [])[:10]
    if ixps:
        col = "{:<30} {:>6} {:>8} {:>10} {:>10}"
        print(_BOLD + col.format("IXP", "IPv6?", "Members", "IPv6 Mbrs", "IPv6 %") + _RESET)
        print("─" * WIDTH)

        for ixp in ixps:
            has_v6 = "✅" if ixp["has_ipv6_lan"] else "❌"
            pct = ixp["ipv6_member_pct"]
            colour = _GREEN if pct >= 75 else (_YELLOW if pct >= 40 else _RED)
            row = col.format(
                ixp["ixp_name"][:30],
                has_v6,
                str(ixp["total_members"]),
                str(ixp["ipv6_members"]),
                f"{pct:.1f}%",
            )
            print(_coloured(row, colour))

        print("─" * WIDTH)
        print()


# ── Section 2: ISP Scorecard ────────────────────────────────────────────

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


def print_deployment_age(deploy_data: dict):
    print(f"\n{_header('SECTION 2.1.2 — IPv6 DEPLOYMENT AGE (RIPEstat)')}")
    print()

    isps = deploy_data.get("isps", [])

    if not isps:
        print("  No deployment age data available.")
        print()
        return

    col = "{:<8} {:<28} {:>8} {:>10} {:>12} {:>10} {:>10}"
    print(_BOLD + col.format(
        "ASN", "ISP", "Mkt Shr", "Adoption", "First Seen", "Age (yrs)", "Reason"
    ) + _RESET)
    print("─" * WIDTH)

    for isp in isps:
        first = isp.get("first_ipv6_seen") or "N/A"
        years = isp.get("deployment_years")
        years_str = f"{years:.1f}" if years is not None else "N/A"
        reason = isp.get("selection_reason", "")
        reason_label = "⭐ Top" if reason == "top_market_share" else "⚠ Laggard"
        adoption = isp.get("ipv6_adoption_pct", 0)
        arch = isp.get("archetype", "OK")
        colour = _ARCHETYPE_COLOUR.get(arch, "")

        if isp.get("error"):
            first = "[error]"
            years_str = "—"

        row = col.format(
            f"AS{isp['asn']}",
            isp["isp"][:28],
            f"{isp['market_share_pct']:.1f}%",
            f"{adoption:.1f}%",
            first,
            years_str,
            reason_label,
        )
        print(_coloured(row, colour))

    print("─" * WIDTH)
    print()
    print(_DIM + "  ⭐ Top = queried due to high market share" + _RESET)
    print(_DIM + "  ⚠ Laggard = queried due to low adoption despite significant market share" + _RESET)
    print(_DIM + "  Source: RIPEstat announced-prefixes (data from 2000–present)" + _RESET)
    print()


# ── Section 3: User-Side Adoption ───────────────────────────────────────

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


# ── Section 4: Web Services ─────────────────────────────────────────────

def print_web_readiness(web_data: dict, country: str):
    print(f"\n{_header('SECTION 4.1 — WEB IPv6 READINESS')}")
    print()

    total = web_data.get("total_domains", 0)
    ipv6 = web_data.get("ipv6_capable", 0)
    ipv4 = web_data.get("ipv4_only", 0)
    pct = web_data.get("ipv6_percentage", 0)

    print(_line("Popular Domains Analyzed:",  str(total)))
    print(_line("IPv6-Reachable:",            f"{ipv6}  ({pct:.1f}%)"))
    print(_line("IPv4-Only:",                 str(ipv4)))
    print(_line("IPv6 Web Readiness:",        _progress_bar(pct)))
    print()


def print_gov_readiness(gov_data: dict):
    print(f"\n{_header('SECTION 4.3.2 — GOVERNMENT IPv6 READINESS')}")
    print()

    gov_tld = gov_data.get("gov_tld", "gov")
    total = gov_data.get("total_gov_domains", 0)
    ipv6 = gov_data.get("ipv6_capable", 0)
    ipv4 = gov_data.get("ipv4_only", 0)
    pct = gov_data.get("ipv6_percentage", 0)

    print(_line("Gov Domain Namespace:",      f".{gov_tld}"))
    print(_line("Gov Domains Assessed:",      str(total)))
    print(_line("IPv6-Capable:",              f"{ipv6}  ({pct:.1f}%)"))
    print(_line("IPv4-Only:",                 str(ipv4)))
    print(_line("Gov IPv6 Readiness:",        _progress_bar(pct)))
    print()


def print_sector_readiness(sector_data: list):
    print(f"\n{_header('SECTION 4.3 — SECTOR IPv6 READINESS')}")
    print()

    col = "{:<14} {:>10} {:>10} {:>14}"
    print(_BOLD + col.format("Sector", "Domains", "IPv6", "Readiness") + _RESET)
    print("─" * WIDTH)

    for entry in sector_data:
        if entry.get("error"):
            continue
        pct = entry.get("ipv6_percentage", 0)
        colour = _GREEN if pct >= 40 else (_YELLOW if pct >= 15 else _RED)
        row = col.format(
            entry.get("sector", "?"),
            str(entry.get("total_domains", 0)),
            str(entry.get("ipv6_capable", 0)),
            f"{pct:.1f}%",
        )
        print(_coloured(row, colour))

    print("─" * WIDTH)
    print()


def print_cdn_correlation(cdn_data: dict):
    print(f"\n{_header('SECTION 4.4 — CDN vs SELF-HOSTED IPv6')}")
    print()

    cdn = cdn_data.get("cdn_domains", 0)
    self_hosted = cdn_data.get("self_hosted", 0)
    ipv6_cdn = cdn_data.get("ipv6_cdn", 0)
    ipv4_self = cdn_data.get("ipv4_only_self_hosted", 0)

    cdn_pct = round((ipv6_cdn / cdn) * 100, 1) if cdn else 0
    self_pct = round((ipv4_self / self_hosted) * 100, 1) if self_hosted else 0

    print(_line("CDN-Backed Domains:",       str(cdn)))
    print(_line("  └ IPv6-Capable:",         f"{ipv6_cdn}  ({cdn_pct}%)"))
    print(_line("Self-Hosted Domains:",      str(self_hosted)))
    print(_line("  └ IPv4-Only:",            f"{ipv4_self}  ({self_pct}%)"))
    print()


# ── Section 5: TLD Health ───────────────────────────────────────────────

def print_tld_health(tld_data: dict, tld_comparison: dict):
    print(f"\n{_header('SECTION 5 — COUNTRY TLD IPv6 HEALTH')}")
    print()

    tld = tld_data.get("tld", "?")
    total = tld_data.get("total_domains", 0)
    ipv6 = tld_data.get("ipv6_enabled_domains", 0)
    pct = tld_data.get("percentage", 0)

    print(_line(f"ccTLD Analyzed:",            tld))
    print(_line("Domains Sampled:",            str(total)))
    print(_line("IPv6-Enabled:",               f"{ipv6}  ({pct:.1f}%)"))
    print(_line("TLD IPv6 Readiness:",         _progress_bar(pct)))
    print()

    # Comparison table
    comparisons = tld_comparison.get("comparisons", [])
    if comparisons:
        print("  Comparative TLD Benchmarks:")
        print()
        print(f"  {'TLD':<10} {'IPv6 Readiness':>16}")
        print("  " + "─" * 28)
        for entry in comparisons:
            print(f"  {entry['tld']:<10} {entry['percentage']:>15.1f}%")
        print()


def print_tld_trend(tld_trend_data: dict):
    print(f"\n{_header('SECTION 5.1.2 — TLD IPv6 TREND')}")
    print()

    trend = tld_trend_data.get("trend", [])
    tld = tld_trend_data.get("tld", "?")
    note = tld_trend_data.get("note", "")

    if not trend:
        print("  No trend data available yet.")
        print()
        return

    print(_line("ccTLD:", tld))
    print(_line("Snapshots Recorded:", str(len(trend))))
    print()

    # Trend table
    col = "{:<14} {:>10} {:>10} {:>12}"
    print(_BOLD + col.format("Date", "Sampled", "IPv6", "Readiness") + _RESET)
    print("─" * WIDTH)

    prev_pct = None
    for entry in trend:
        pct = entry["pct"]
        if prev_pct is not None:
            delta = pct - prev_pct
            chg = f"  ({delta:+.1f} pp)"
        else:
            chg = ""
        colour = _GREEN if pct >= 40 else (_YELLOW if pct >= 20 else _RED)
        row = col.format(
            entry["date"],
            str(entry["total"]),
            str(entry["ipv6"]),
            f"{pct:.1f}%{chg}",
        )
        print(_coloured(row, colour))
        prev_pct = pct

    print("─" * WIDTH)
    print()
    print(_DIM + f"  {note}" + _RESET)
    print()


def print_nameserver_health(ns_data: dict, glue_data: dict):
    print(f"\n{_header('SECTION 5.2 — NAMESERVER IPv6 REACHABILITY')}")
    print()

    ns_total = ns_data.get("total_nameservers", 0)
    ns_ipv6 = ns_data.get("ipv6_enabled_nameservers", 0)
    ns_pct = ns_data.get("percentage", 0)

    glue_total = glue_data.get("total_glue_nameservers", 0)
    glue_ipv6 = glue_data.get("ipv6_enabled_glue", 0)
    glue_pct = glue_data.get("percentage", 0)

    print(_line("Auth. Nameservers:",          str(ns_total)))
    print(_line("  └ IPv6-Reachable:",         f"{ns_ipv6}  ({ns_pct:.1f}%)"))
    print(_line("NS IPv6 Reachability:",       _progress_bar(ns_pct)))
    print()
    print(_line("Glue-style Nameservers:",     str(glue_total)))
    print(_line("  └ IPv6-Capable:",           f"{glue_ipv6}  ({glue_pct:.1f}%)"))
    print(_line("Glue IPv6 Readiness:",        _progress_bar(glue_pct)))
    print()


# ── Executive Summary ───────────────────────────────────────────────────

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
    step = 0
    total_steps = 15

    def _step(msg):
        nonlocal step
        step += 1
        print(f"\n  [{step}/{total_steps}] {msg}", end=" ", flush=True)

    # ── Banner ───────────────────────────────────────────────────────────────
    print()
    print(_hr())
    print(_BOLD + f"  IPv6 POLICY ENGINE — COUNTRY REPORT: {country}" + _RESET)
    print(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Data Year : {args.year}")
    print(f"  Sources   : ISOC Pulse API · Internet Yellow Pages (IYP) Neo4j")
    print(f"  Framework : ISOC IRI — Security Pillar → Enabling Technologies → IPv6")
    print(_hr())

    # ── Section 1: Core Infrastructure ────────────────────────────────────────
    _step(f"Measuring RPKI coverage for {country}...")
    rpki_data = get_rpki_coverage(country)
    print("done.")
    print_rpki(rpki_data)

    _step(f"Identifying weakest RPKI ISPs...")
    isp_rpki_data = get_isp_rpki_coverage(country)
    print("done.")
    print_isp_rpki(isp_rpki_data)

    _step(f"Assessing IPv6 upstream connectivity...")
    upstream_data = get_ipv6_upstream_connectivity(country)
    print("done.")
    print_upstream(upstream_data)

    _step(f"Analyzing IXP IPv6 peering...")
    ixp_data = get_ixp_ipv6_peering(country)
    print("done.")
    print_ixp_peering(ixp_data)

    # ── Section 2: Scorecard ─────────────────────────────────────────────────
    _step(f"Building ISP scorecard for {country}...")
    scorecard = build_scorecard(country, year=args.year)

    if scorecard.get("error"):
        print(f"\n  [ERROR] {scorecard['error']}")
        sys.exit(1)

    print("done.")
    print_scorecard(scorecard)

    _step(f"Fetching IPv6 deployment age (RIPEstat)...")
    deploy_age_data = get_ipv6_deployment_age(scorecard)
    print("done.")
    print_deployment_age(deploy_age_data)

    # ── Section 3: Trend ─────────────────────────────────────────────────────
    _step(f"Fetching adoption trend ({args.trend_start}–{args.year})...")
    trend = get_adoption_trend(country, start_year=args.trend_start, end_year=args.year)
    print("done.")
    print_trend(trend, country)

    _step(f"Computing regional comparison...")
    comparison = get_regional_comparison(country, year=args.year)
    print("done.")
    print_comparison(comparison)

    # ── Section 4: Web Services ──────────────────────────────────────────────
    _step(f"Analyzing web IPv6 readiness (.{country.lower()} domains)...")
    web_data = get_web_ipv6_readiness(country)
    print("done.")
    print_web_readiness(web_data, country)

    _step(f"Checking government IPv6 readiness...")
    gov_data = get_government_ipv6_readiness(country)
    print("done.")
    print_gov_readiness(gov_data)

    _step(f"Scanning sector IPv6 readiness...")
    banking_data = get_sector_ipv6_readiness(
        "Banking",
        ["bank", "banking", "finance", "credit"],
        country_code=country,
    )
    news_data = get_sector_ipv6_readiness(
        "News",
        ["news", "times", "media"],
        country_code=country,
    )
    education_data = get_sector_ipv6_readiness(
        "Education",
        ["edu", "college", "university"],
        country_code=country,
    )
    ecommerce_data = get_sector_ipv6_readiness(
        "Ecommerce",
        ["shop", "store"],
        country_code=country,
    )
    sector_data = [banking_data, news_data, education_data, ecommerce_data]
    print("done.")
    print_sector_readiness(sector_data)

    cdn_data = get_cdn_ipv6_correlation(country)
    print_cdn_correlation(cdn_data)

    # ── Section 5: TLD Health ────────────────────────────────────────────────
    _step(f"Measuring TLD IPv6 health...")
    tld_data = get_tld_ipv6_health(country)
    tld_comparison_data = compare_tld_ipv6_readiness(country)
    print("done.")
    print_tld_health(tld_data, tld_comparison_data)

    _step(f"Recording TLD IPv6 trend snapshot...")
    tld_trend_data = get_tld_ipv6_trend(country, tld_data=tld_data)
    print("done.")
    print_tld_trend(tld_trend_data)

    _step(f"Checking nameserver IPv6 reachability...")
    nameserver_data = get_nameserver_ipv6_health(country)
    glue_data = get_glue_record_ipv6_health(country)
    print("done.")
    print_nameserver_health(nameserver_data, glue_data)

    # ── Executive Summary ─────────────────────────────────────────────────────
    _step(f"Generating executive summary...")
    summary_text = generate_executive_summary(scorecard)
    print("done.")
    print_executive_summary(summary_text)

    # ── Export ────────────────────────────────────────────────────────────────
    if not args.no_export:
        print()
        try:
            filepath = export_policy_brief(
                scorecard    = scorecard,
                summary_text = summary_text,
                trend        = trend,
                comparison   = comparison,
                rpki_data    = rpki_data,
                isp_rpki_data  = isp_rpki_data,
                upstream_data  = upstream_data,
                ixp_data       = ixp_data,
                deploy_age_data = deploy_age_data,
                tld_data       = tld_data,
                tld_comparison_data  = tld_comparison_data,
                tld_trend_data = tld_trend_data,
                nameserver_data = nameserver_data,
                glue_data = glue_data,
                web_data= web_data,
                gov_data = gov_data,
                sector_data= sector_data,
                cdn_data = cdn_data,
            )
            print(_hr("─"))
            print(f"  [EXPORT] Policy brief saved →  {filepath}")
            print(_hr("─"))
        except Exception as e:
            print(f"\n  [EXPORT ERROR] Report generation failed: {e}")
            print(f"  Terminal output above is still valid.")

    print()
    print(_hr())
    print()


if __name__ == "__main__":
    main()
