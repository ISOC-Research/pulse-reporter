"""
ipv6_engine.py
==============
Core IPv6 Policy Engine for ISOC Pulse × IYP integration.
Covers Framework Sections 2 (ISP Deployment) and 3 (User-Side Adoption).

All functions are pure data logic — no I/O, no print statements.
Designed to be imported by both the Flask backend and the CLI report script.

Authors : Rahul Rajesh, Ron Prajoth, Aditya Menon
Mentor  : Amreesh Phokeer (Internet Society)
"""

import os
import sys
import pathlib
from datetime import datetime
from typing import Optional

# ── Path resolution (works from any working directory) ──────────────────────
_ROOT = pathlib.Path(__file__).resolve().parents[1]   # pulse-reporter/
_SRC  = pathlib.Path(__file__).resolve().parent       # pulse-reporter/request_for_YPI/

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv
load_dotenv(_ROOT / ".env")

from request_for_YPI.src.request_IYP.request_testing import execute_cypher_test
from request_for_YPI.pulse_service import (
    extract_all_countries_indicator,
    get_data_from_year,
    get_indicator_value,
)


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS — Archetype thresholds (per Amreesh's policy rules)
# ═══════════════════════════════════════════════════════════════════════════

BOTTLENECK_MARKET_SHARE  = 0.15   # 15% — Category D trigger
BOTTLENECK_ADOPTION_CAP  = 0.20   # 20% adoption ceiling for D
LAGGARD_ADOPTION_CAP     = 0.05   # 5%  — Category C trigger

SEVERITY_CRITICAL  = 1000         # Customer Cone Size thresholds
SEVERITY_HIGH      = 200
SEVERITY_MEDIUM    = 50

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — CORE INFRASTRUCTURE / RPKI ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════

def get_rpki_coverage(country_code: str) -> dict:
    """
    Section 1.1.3 — Measure IPv6 RPKI coverage for a country.

    Returns:
    {
        "country": str,
        "total_ipv6_prefixes": int,
        "rpki_covered_prefixes": int,
        "coverage_pct": float,
        "error": str | None
    }
    """

    country_code = country_code.upper()

    query = f"""
    MATCH (c:Country {{country_code: '{country_code}'}})
          <-[:POPULATION]-(a:AS)

    MATCH (a)-[:ORIGINATE]->(b:BGPPrefix)
    WHERE b.prefix CONTAINS ':'

    OPTIONAL MATCH (b)-[:PART_OF]->(r:RPKIPrefix)

    RETURN
        COUNT(DISTINCT b) AS total_ipv6_prefixes,
        COUNT(DISTINCT r) AS rpki_covered_prefixes
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": f"IYP query failed: {result['error']}"
        }

    if not result["data"]:
        return {
            "error": f"No IPv6 prefix data found for {country_code}"
        }

    row = result["data"][0]

    total = row.get("total_ipv6_prefixes", 0) or 0
    covered = row.get("rpki_covered_prefixes", 0) or 0

    coverage_pct = round((covered / total) * 100, 2) if total > 0 else 0.0

    return {
        "country": country_code,
        "total_ipv6_prefixes": total,
        "rpki_covered_prefixes": covered,
        "coverage_pct": coverage_pct,
        "error": None,
    }

def get_isp_rpki_coverage(country_code: str) -> dict:
    """
    Section 1.1.3.1 — ISP-level IPv6 RPKI coverage analysis.

    Returns:
    {
        "country": str,
        "isps": [
            {
                "asn": int,
                "isp": str,
                "total_ipv6_prefixes": int,
                "rpki_covered_prefixes": int,
                "coverage_pct": float
            }
        ]
    }
    """

    country_code = country_code.upper()

    query = f"""
    MATCH (c:Country {{country_code: '{country_code}'}})
          <-[:POPULATION]-(a:AS)

    OPTIONAL MATCH (a)-[:NAME]->(n:Name)

    MATCH (a)-[:ORIGINATE]->(b:BGPPrefix)
    WHERE b.prefix CONTAINS ':'

    OPTIONAL MATCH (b)-[:PART_OF]->(r:RPKIPrefix)

    WITH
        a,
        collect(DISTINCT n.name)[0] AS isp_name,
        COUNT(DISTINCT b) AS total_ipv6_prefixes,
        COUNT(DISTINCT r) AS rpki_covered_prefixes

    RETURN
        a.asn AS asn,
        COALESCE(isp_name, a.org_name, toString(a.asn)) AS isp,
        total_ipv6_prefixes,
        rpki_covered_prefixes
        ORDER BY total_ipv6_prefixes DESC
        LIMIT 25
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": f"IYP query failed: {result['error']}"
        }

    isps = []

    for row in result["data"]:
        total = row.get("total_ipv6_prefixes", 0) or 0
        covered = row.get("rpki_covered_prefixes", 0) or 0

        coverage_pct = round((covered / total) * 100, 2) if total > 0 else 0.0

        isps.append({
            "asn": row.get("asn"),
            "isp": row.get("isp"),
            "total_ipv6_prefixes": total,
            "rpki_covered_prefixes": covered,
            "coverage_pct": coverage_pct,
        })

    return {
        "country": country_code,
        "isps": isps,
        "error": None,
    }

def get_ipv6_upstream_connectivity(country_code: str) -> dict:
    """
    Section 1.2 — Measure IPv6-capable upstream connectivity.

    Determines which ISPs depend on upstream ASNs
    that originate IPv6 prefixes.
    """

    country_code = country_code.upper()

    query = f"""
    MATCH (c:Country {{country_code: '{country_code}'}})
          <-[:POPULATION]-(a:AS)

    OPTIONAL MATCH (a)-[:NAME]->(n:Name)

    OPTIONAL MATCH (a)-[:DEPENDS_ON]->(upstream:AS)

    OPTIONAL MATCH (upstream)-[:ORIGINATE]->(b:BGPPrefix)
    WHERE b.prefix CONTAINS ':'

    WITH
        a,
        collect(DISTINCT n.name)[0] AS isp_name,
        COUNT(DISTINCT b) AS upstream_ipv6_prefixes

    RETURN
        a.asn AS asn,
        COALESCE(isp_name, a.org_name, toString(a.asn)) AS isp,
        upstream_ipv6_prefixes,
        CASE
            WHEN upstream_ipv6_prefixes > 0 THEN true
            ELSE false
        END AS has_ipv6_upstream
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": f"IYP query failed: {result['error']}"
        }

    isps = result["data"]

    total_isps = len(isps)

    ipv6_ready = sum(
        1 for isp in isps
        if isp.get("has_ipv6_upstream")
    )

    pct = round((ipv6_ready / total_isps) * 100, 2) if total_isps > 0 else 0.0

    return {
        "country": country_code,
        "total_isps": total_isps,
        "ipv6_upstream_ready": ipv6_ready,
        "percentage": pct,
        "isps": isps,
        "error": None,
    }

def get_tld_ipv6_health(country_code: str) -> dict:
    """
    Section 5.1 — ccTLD IPv6 readiness analysis.

    Measures how many country-code TLD domains
    resolve to IPv6-enabled infrastructure.
    """

    country_code = country_code.upper()

    tld = country_code.lower()

    query = f"""
    MATCH (d:DomainName)

    WHERE d.name ENDS WITH '.{tld}'

    WITH d
    LIMIT 5000

    OPTIONAL MATCH (d)-[:PART_OF]-(h:HostName)
                    -[:RESOLVES_TO]->(ip:IP {{af: 6}})

    WITH
        d,
        COUNT(ip) > 0 AS has_ipv6

    RETURN
        COUNT(d) AS total_domains,
        SUM(CASE WHEN has_ipv6 THEN 1 ELSE 0 END) AS ipv6_enabled_domains
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": f"IYP query failed: {result['error']}"
        }

    row = result["data"][0]

    total = row.get("total_domains", 0) or 0
    ipv6_enabled = row.get("ipv6_enabled_domains", 0) or 0

    percentage = (
        round((ipv6_enabled / total) * 100, 2)
        if total > 0 else 0.0
    )

    return {
        "country": country_code,
        "tld": f".{tld}",
        "total_domains": total,
        "ipv6_enabled_domains": ipv6_enabled,
        "percentage": percentage,
        "error": None,
    }

def analyze_tld_ipv6_readiness(tld: str, sample_limit: int = 5000) -> dict:
    """
    Analyze IPv6 readiness for a given TLD.

    Example:
        .in
        .fr
        .com
    """

    tld = tld.lower().replace(".", "")

    query = f"""
    MATCH (d:DomainName)

    WHERE d.name ENDS WITH '.{tld}'

    WITH d
    LIMIT {sample_limit}

    OPTIONAL MATCH (d)-[:PART_OF]-(h:HostName)
                    -[:RESOLVES_TO]->(ip:IP {{af: 6}})

    WITH
        d,
        COUNT(ip) > 0 AS has_ipv6

    RETURN
        COUNT(d) AS total_domains,
        SUM(CASE WHEN has_ipv6 THEN 1 ELSE 0 END) AS ipv6_enabled_domains
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": result["error"]
        }

    row = result["data"][0]

    total = row.get("total_domains", 0) or 0
    enabled = row.get("ipv6_enabled_domains", 0) or 0

    pct = round((enabled / total) * 100, 2) if total > 0 else 0.0

    return {
        "tld": f".{tld}",
        "total_domains": total,
        "ipv6_enabled_domains": enabled,
        "percentage": pct,
    }

def compare_tld_ipv6_readiness(base_country: str) -> dict:
    """
    Section 5.1.1 — Compare ccTLD IPv6 readiness
    against .com and peer TLDs.
    """

    base_country = base_country.upper()

    tld_map = {
        "IN": [".in", ".com", ".fr", ".de"],
        "FR": [".fr", ".com", ".de", ".in"],
        "DE": [".de", ".com", ".fr", ".in"],
    }

    comparison_tlds = tld_map.get(
        base_country,
        [f".{base_country.lower()}", ".com"]
    )

    results = []

    for tld in comparison_tlds:
        results.append(
            analyze_tld_ipv6_readiness(tld)
        )

    return {
        "country": base_country,
        "comparisons": results,
    }


def get_nameserver_ipv6_health(country_code: str,
                               sample_limit: int = 5000) -> dict:
    """
    Section 5.2 — Measure IPv6 reachability
    of authoritative nameservers for a ccTLD.
    """

    tld = country_code.lower()

    query = f"""
    MATCH (d:DomainName)-[:MANAGED_BY]->(ns:AuthoritativeNameServer)

    WHERE d.name ENDS WITH '.{tld}'

    WITH DISTINCT d, ns
    LIMIT {sample_limit}

    OPTIONAL MATCH (ns)-[:RESOLVES_TO]->(ip:IP {{af: 6}})

    WITH
        ns,
        COUNT(ip) > 0 AS has_ipv6

    RETURN
        COUNT(DISTINCT ns) AS total_nameservers,
        SUM(CASE WHEN has_ipv6 THEN 1 ELSE 0 END)
            AS ipv6_enabled_nameservers
    """
    
    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": result["error"]
        }

    row = result["data"][0]

    total = row.get("total_nameservers", 0) or 0
    enabled = row.get("ipv6_enabled_nameservers", 0) or 0

    pct = round((enabled / total) * 100, 2) if total > 0 else 0.0

    return {
        "country": country_code.upper(),
        "total_nameservers": total,
        "ipv6_enabled_nameservers": enabled,
        "percentage": pct,
        "error": None
    }

def get_glue_record_ipv6_health(country_code: str,
                                sample_limit: int = 5000) -> dict:
    """
    Section 5.2.1 — Approximate glue-record IPv6 readiness.

    Detects in-zone authoritative nameservers
    and checks whether they resolve to IPv6.
    """

    tld = country_code.lower()

    query = f"""
    MATCH (d:DomainName)-[:MANAGED_BY]->(ns:AuthoritativeNameServer)

    WHERE d.name ENDS WITH '.{tld}'

    WITH DISTINCT d, ns
    LIMIT {sample_limit}

    WITH
        d,
        ns,

        CASE
            WHEN ns.name ENDS WITH d.name
            THEN true
            ELSE false
        END AS is_glue_candidate

    WHERE is_glue_candidate = true

    OPTIONAL MATCH (ns)-[:RESOLVES_TO]->(ip:IP {{af: 6}})

    WITH
        ns,
        COUNT(ip) > 0 AS has_ipv6

    RETURN
        COUNT(DISTINCT ns) AS total_glue_nameservers,
        SUM(CASE WHEN has_ipv6 THEN 1 ELSE 0 END)
            AS ipv6_enabled_glue
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {
            "error": result["error"]
        }

    row = result["data"][0]

    total = row.get("total_glue_nameservers", 0) or 0
    enabled = row.get("ipv6_enabled_glue", 0) or 0

    pct = round((enabled / total) * 100, 2) if total > 0 else 0.0

    return {
        "country": country_code.upper(),
        "total_glue_nameservers": total,
        "ipv6_enabled_glue": enabled,
        "percentage": pct,
        "error": None
    }



# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — ISP DEPLOYMENT SCORECARD
# ═══════════════════════════════════════════════════════════════════════════

def _query_asn_ipv6_prefixes(country_code: str) -> dict:
    """
    Pull each ASN in the country with its IPv6 prefix count,
    market share (APNIC population proxy), customer cone size,
    and human-readable name.
    Returns the raw execute_cypher_test result dict.
    """
    query = f"""
    MATCH (c:Country {{country_code: '{country_code.upper()}'}})<-[r:POPULATION]-(a:AS)
    WHERE r.percent IS NOT NULL

    OPTIONAL MATCH (a)-[:NAME]->(n:Name)
    WITH a, r, collect(DISTINCT n.name)[0] AS isp_name

    OPTIONAL MATCH (a)-[:ORIGINATE]->(p:Prefix)
    WHERE p.prefix CONTAINS ':'

    WITH a, r, isp_name, count(p) AS ipv6_prefix_count

    OPTIONAL MATCH (a)-[rank:RANK]->(rk:Ranking {{name:'CAIDA ASRank'}})

    RETURN
        a.asn                          AS asn,
        COALESCE(isp_name, a.org_name, toString(a.asn)) AS isp,
        r.percent                      AS market_share_pct,
        ipv6_prefix_count              AS ipv6_prefixes,
        rank['cone:numberAsns']        AS cone_size
    ORDER BY market_share_pct DESC
    LIMIT 25
    """
    return execute_cypher_test(query)


def _classify_archetype(ipv6_prefixes: int, market_share: float,
                         ipv6_adoption: float) -> str:
    """
    Assign a policy archetype to a single ISP.

    Category D (Bottleneck) takes priority — checked first.

    A — Ghost    : 0 IPv6 prefixes announced (no BGP presence)
    B — Hoarder  : Has allocation but 0 BGP announcements
                   NOTE: IYP only tracks announced prefixes, not allocated-but-
                   unannounced blocks. Category B is flagged as 'HOARDER*'
                   with an asterisk to indicate this needs RIR cross-check.
                   For data we can confirm from IYP, treat as equivalent to A.
    C — Laggard  : BGP active (>0 prefixes) but adoption < 5%
    D — Bottleneck: Market share >= 15% AND adoption < 20%
    OK — Compliant: Everything else
    """
    # D is the highest-priority classification
    if market_share >= BOTTLENECK_MARKET_SHARE and ipv6_adoption < BOTTLENECK_ADOPTION_CAP:
        return "D"

    if ipv6_prefixes == 0:
        return "A"   # Ghost — no IPv6 in BGP at all

    if ipv6_prefixes > 0 and ipv6_adoption < LAGGARD_ADOPTION_CAP:
        return "C"   # Laggard — has BGP presence, but users aren't on it

    return "OK"


def _archetype_label(code: str) -> str:
    labels = {
        "A":  "Ghost (No Allocation)",
        "C":  "Laggard (No Traffic)",
        "D":  "Bottleneck (High-Impact)",
        "OK": "Compliant",
    }
    return labels.get(code, code)


def _archetype_intervention(code: str) -> str:
    interventions = {
        "A":  "Regulatory mandate for RIR membership / govt IPv6 subsidy",
        "C":  "Last Mile: target CPE/router hardware import standards",
        "D":  "PRIORITY — Direct government engagement; ISP blocks national goals",
        "OK": "No immediate intervention required",
    }
    return interventions.get(code, "Unknown")


def build_scorecard(country_code: str, year: int = 2024) -> dict:
    """
    Main Section 2 function.
    Fuses IYP (prefixes, cone size) + Pulse API (national adoption)
    and assigns each ISP to a policy archetype.

    Returns:
    {
        "country": str,
        "year": int,
        "national_adoption": float,          # 0–1
        "isps": [
            {
                "asn": int,
                "isp": str,
                "market_share_pct": float,   # 0–100 scale (APNIC)
                "ipv6_prefixes": int,
                "cone_size": int,
                "ipv6_adoption_est": float,  # 0–1, estimated
                "archetype": str,            # A / C / D / OK
                "archetype_label": str,
                "intervention": str,
                "severity": str,             # Critical/High/Medium/Low
                "projected_impact_pp": float # percentage-point gain if this ISP hits 100%
            },
            ...
        ],
        "summary": {
            "total_isps": int,
            "ghost_count": int,
            "laggard_count": int,
            "bottleneck_count": int,
            "compliant_count": int,
            "combined_laggard_share_pct": float,
            "combined_underserved_pct": float,
        },
        "error": str | None
    }
    """
    country_code = country_code.upper()

    # ── 1. National IPv6 adoption from Pulse API ─────────────────────────
    all_ipv6 = extract_all_countries_indicator(year, "ipv6")
    nat_entry = next((x for x in all_ipv6 if x["country"] == country_code), None)

    if nat_entry is None:
        return {"error": f"No Pulse API data for {country_code} in {year}"}

    national_adoption = nat_entry["average"]   # already 0–1 float

    # ── 2. IYP: per-ASN prefix + market share data ───────────────────────
    result = _query_asn_ipv6_prefixes(country_code)

    if not result["success"]:
        return {"error": f"IYP query failed: {result['error']}"}

    if not result["data"]:
        return {"error": f"No ASN data found in IYP for {country_code}"}

    # ── 3. Build enriched ISP list ────────────────────────────────────────
    isps = []

    for row in result["data"]:
        asn             = row.get("asn")
        isp             = row.get("isp") or f"AS{asn}"
        market_share    = row.get("market_share_pct") or 0.0
        ipv6_prefixes   = row.get("ipv6_prefixes") or 0
        cone_size       = row.get("cone_size") or 0

        # Market share normalised to 0–1 for formula use
        market_share_norm = market_share / 100.0

        # IPv6 adoption estimate for this ISP.
        # We use national adoption as baseline, adjusted by relative market share.
        # Large ISPs pull the average up or down — we model their adoption
        # proportionally. If they have 0 prefixes, their adoption is 0.
        if ipv6_prefixes == 0:
            ipv6_adoption_est = 0.0
        else:
            # Adjustment: bigger ISPs pull the national average; smaller ones follow.
            # Capped at [0, 1].
            centred    = (market_share_norm - 0.5)
            adjustment = centred * 0.4
            ipv6_adoption_est = max(0.0, min(1.0,
                                   national_adoption * (1 + adjustment)))

        # ── Archetype classification ─────────────────────────────────────
        archetype = _classify_archetype(
            ipv6_prefixes, market_share_norm, ipv6_adoption_est
        )

        # ── Severity (based on Customer Cone Size) ───────────────────────
        if cone_size >= SEVERITY_CRITICAL:
            severity = "Critical"
        elif cone_size >= SEVERITY_HIGH:
            severity = "High"
        elif cone_size >= SEVERITY_MEDIUM:
            severity = "Medium"
        else:
            severity = "Low"

        # ── Projected national impact (impact formula) ───────────────────
        # A_new = A_nat + M_z × (1.0 - A_z)
        projected_new_national = national_adoption + (
            market_share_norm * (1.0 - ipv6_adoption_est)
        )
        impact_pp = (projected_new_national - national_adoption) * 100  # in pp

        isps.append({
            "asn":                asn,
            "isp":                isp,
            "market_share_pct":   round(market_share, 2),
            "ipv6_prefixes":      ipv6_prefixes,
            "cone_size":          cone_size,
            "ipv6_adoption_est":  round(ipv6_adoption_est, 4),
            "archetype":          archetype,
            "archetype_label":    _archetype_label(archetype),
            "intervention":       _archetype_intervention(archetype),
            "severity":           severity,
            "projected_impact_pp": round(impact_pp, 2),
        })

    # ── 4. Summary statistics ─────────────────────────────────────────────
    ghost_isps      = [x for x in isps if x["archetype"] == "A"]
    laggard_isps    = [x for x in isps if x["archetype"] == "C"]
    bottleneck_isps = [x for x in isps if x["archetype"] == "D"]
    compliant_isps  = [x for x in isps if x["archetype"] == "OK"]

    # Combined underserved share = all non-compliant ISPs
    non_compliant   = ghost_isps + laggard_isps + bottleneck_isps
    combined_underserved = sum(x["market_share_pct"] for x in non_compliant)

    # Laggard-specific share (Cat B+C for policy reporting)
    combined_laggard = sum(x["market_share_pct"] for x in laggard_isps + ghost_isps)

    return {
        "country":           country_code,
        "year":              year,
        "national_adoption": round(national_adoption, 4),
        "isps":              isps,
        "summary": {
            "total_isps":               len(isps),
            "ghost_count":              len(ghost_isps),
            "laggard_count":            len(laggard_isps),
            "bottleneck_count":         len(bottleneck_isps),
            "compliant_count":          len(compliant_isps),
            "combined_laggard_share_pct":   round(combined_laggard, 2),
            "combined_underserved_pct":     round(combined_underserved, 2),
        },
        "error": None,
    }


def get_combined_laggard_share(scorecard: dict) -> float:
    """
    Returns the combined market share % of all non-compliant ISPs
    (Categories A, C, D) — i.e., the share of users currently underserved.
    """
    return scorecard.get("summary", {}).get("combined_underserved_pct", 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — EXECUTIVE SUMMARY GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

def generate_executive_summary(scorecard: dict) -> str:
    """
    Generates a single-paragraph executive summary from a scorecard.
    Highlights Category D (Bottleneck) ISPs and projects national impact
    using the exact formula: A_new = A_nat + M_z × (1.0 - A_z)

    Returns a plain-text paragraph string.
    """
    if scorecard.get("error"):
        return f"[ERROR] Cannot generate summary: {scorecard['error']}"

    country         = scorecard["country"]
    nat_adoption    = scorecard["national_adoption"]
    nat_pct         = round(nat_adoption * 100, 1)
    summary_data    = scorecard["summary"]
    isps            = scorecard["isps"]

    bottlenecks = [x for x in isps if x["archetype"] == "D"]
    ghosts      = [x for x in isps if x["archetype"] == "A"]
    laggards    = [x for x in isps if x["archetype"] == "C"]

    underserved = summary_data["combined_underserved_pct"]

    lines = [
        f"{country} currently has a national IPv6 adoption rate of {nat_pct}%, "
        f"with {underserved:.1f}% of the subscriber market served by ISPs "
        f"classified as non-compliant."
    ]

    # Category D — highest priority
    if bottlenecks:
        d_parts = []
        for isp in bottlenecks:
            a_nat  = nat_adoption
            m_z    = isp["market_share_pct"] / 100.0
            a_z    = isp["ipv6_adoption_est"]
            a_new  = a_nat + m_z * (1.0 - a_z)
            gain   = round((a_new - a_nat) * 100, 1)
            new_pct = round(a_new * 100, 1)
            d_parts.append(
                f"AS{isp['asn']} ({isp['isp']}, {isp['market_share_pct']:.1f}% market share): "
                f"targeting this provider alone would increase national adoption "
                f"from {nat_pct}% to {new_pct}% (+{gain} percentage points)"
            )
        lines.append(
            f"PRIORITY ACTION — {len(bottlenecks)} high-impact "
            f"bottleneck provider(s) identified: " + "; ".join(d_parts) + "."
        )

    # Category A — Ghost ISPs
    if ghosts:
        ghost_share = sum(x["market_share_pct"] for x in ghosts)
        lines.append(
            f"{len(ghosts)} ISP(s) (covering {ghost_share:.1f}% of the market) "
            f"have zero IPv6 prefixes in the global routing table and require "
            f"immediate regulatory intervention for RIR membership."
        )

    # Category C — Laggards
    if laggards:
        lag_share = sum(x["market_share_pct"] for x in laggards)
        lines.append(
            f"{len(laggards)} ISP(s) (covering {lag_share:.1f}% of the market) "
            f"have active BGP announcements but near-zero user-side adoption, "
            f"indicating a last-mile CPE or hardware configuration problem "
            f"requiring targeted equipment standards enforcement."
        )

    if not bottlenecks and not ghosts and not laggards:
        lines.append(
            f"All major ISPs are currently classified as compliant. "
            f"Focus should shift to sustaining adoption growth and improving "
            f"RPKI security hygiene."
        )

    return " ".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — USER-SIDE ADOPTION
# ═══════════════════════════════════════════════════════════════════════════

def get_adoption_trend(country_code: str,
                       start_year: int = 2020,
                       end_year:   int = 2024) -> list:
    """
    Section 3.1.2 — IPv6 adoption trend over multiple years.
    """

    country_code = country_code.upper()
    trend = []

    for year in range(start_year, end_year + 1):

        try:
            entries = extract_all_countries_indicator(year, "ipv6")

            entry = next(
                (x for x in entries if x["country"] == country_code),
                None
            )

            if entry:
                raw = entry["average"]

                # Filter anomalous Pulse values (e.g. 1.0 / 100%)
                # which likely indicate corrupted or placeholder data
                if raw >= 0.98:
                    adoption = None
                else:
                    adoption = round(raw, 4)

            else:
                adoption = None

        except Exception:
            adoption = None

        trend.append({
            "year": year,
            "adoption": adoption
        })

    return trend

def get_regional_comparison(country_code: str,
                             year: int = 2024,
                             top_n: int = 5) -> dict:
    """
    Section 3.1.3 — Position the country vs. regional peers and global avg.

    Returns:
    {
        "reference": {"country": str, "adoption": float, "adoption_pct": float},
        "global_average": float,
        "global_rank": int,           # 1 = best
        "total_countries": int,
        "above_global_avg": bool,
        "closest_peers": [            # top_n countries nearest in adoption score
            {"country": str, "adoption": float, "distance": float},
            ...
        ]
    }
    """
    country_code = country_code.upper()
    all_data = extract_all_countries_indicator(year, "ipv6")

    ref = next((x for x in all_data if x["country"] == country_code), None)
    if not ref:
        return {"error": f"No data for {country_code} in {year}"}

    ref_val = ref["average"]

    valid = [x for x in all_data if x["average"] is not None]
    valid_sorted = sorted(valid, key=lambda x: x["average"], reverse=True)

    global_avg = sum(x["average"] for x in valid) / len(valid) if valid else 0.0

    # Rank (1-indexed, 1 = highest adoption)
    rank = next(
        (i + 1 for i, x in enumerate(valid_sorted) if x["country"] == country_code),
        None
    )

    # Closest peers by adoption distance (excluding self)
    peers = sorted(
        [x for x in valid if x["country"] != country_code],
        key=lambda x: abs(x["average"] - ref_val)
    )[:top_n]

    return {
        "reference": {
            "country":      country_code,
            "adoption":     round(ref_val, 4),
            "adoption_pct": round(ref_val * 100, 1),
        },
        "global_average":     round(global_avg, 4),
        "global_average_pct": round(global_avg * 100, 1),
        "global_rank":        rank,
        "total_countries":    len(valid),
        "above_global_avg":   ref_val > global_avg,
        "closest_peers": [
            {
                "country":    p["country"],
                "adoption":   round(p["average"], 4),
                "adoption_pct": round(p["average"] * 100, 1),
                "distance":   round(abs(p["average"] - ref_val), 4),
            }
            for p in peers
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# EXPORT — POLICY BRIEF (Markdown)
# ═══════════════════════════════════════════════════════════════════════════

def export_policy_brief(
    scorecard:   dict,
    summary_text: str,
    trend:       list,
    comparison:  dict,
    rpki_data:   dict,
    isp_rpki_data: dict,
    upstream_data: dict,
    tld_data: dict,
    tld_comparison_data: dict,
    nameserver_data: dict,
    glue_data: dict,
    output_dir:  Optional[str] = None,
) -> str:
    """
    Exports a structured Markdown policy brief.
    Returns the filepath of the saved file.
    """
    country  = scorecard.get("country", "XX")
    year     = scorecard.get("year", 2024)
    date_str = datetime.now().strftime("%Y%m%d_%H%M")

    if output_dir is None:
        output_dir = str(_ROOT / "reports")

    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"IPv6_{country}_{date_str}.md")

    nat_pct  = round(scorecard.get("national_adoption", 0) * 100, 1)
    isps     = scorecard.get("isps", [])
    stats    = scorecard.get("summary", {})

    lines = [
        f"# IPv6 Policy Brief — {country}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Data Sources:** ISOC Pulse API {year} · Internet Yellow Pages (IYP) Neo4j  ",
        f"**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        summary_text,
        "",
        "---",
        "",
        "## Section 1 — Core Infrastructure / RPKI Security",
        "",
        f"**Total IPv6 Prefixes:** {rpki_data.get('total_ipv6_prefixes', 0):,}  ",
        f"**RPKI-Covered Prefixes:** {rpki_data.get('rpki_covered_prefixes', 0):,}  ",
        f"**RPKI Coverage:** {rpki_data.get('coverage_pct', 0):.2f}%  ",
        "",
        "> RPKI coverage measures the percentage of IPv6 routing prefixes",
        "> protected using Route Origin Authorization (ROA) records for routing security.",
        "",
        "---",
        "",
                "### ISPs with Weak RPKI Coverage",
        "",
        "| ISP | IPv6 Prefixes | RPKI Coverage |",
        "|-----|---------------|---------------|",

        *[
            f"| {isp['isp'][:40]} | "
            f"{isp['total_ipv6_prefixes']} | "
            f"{isp['coverage_pct']:.2f}% |"
            for isp in sorted(
                isp_rpki_data.get("isps", []),
                key=lambda x: x["coverage_pct"]
            )[:5]
        ],

        "",
        "> Several major networks continue to exhibit weak RPKI",
        "> adoption despite significant IPv6 routing presence.",
        "",
        "---",
        "",
                "### Preliminary IPv6 Upstream Connectivity",
        "",
        f"**ISPs Assessed:** {upstream_data.get('total_isps', 0)}  ",
        f"**IPv6-Capable Upstream Reachability:** {upstream_data.get('percentage', 0):.2f}%  ",
        "",
        "> Preliminary graph-based analysis suggests that most assessed",
        "> ISPs maintain upstream dependencies connected to IPv6-capable",
        "> transit or peering networks.",
        "",
        "> NOTE: This metric is currently experimental and based on",
        "> inferred AS dependency relationships within the IYP graph.",
        "",
        "---",
        "",
        "## Section 2 — ISP Compliance Scorecard",
        "",
        f"**National IPv6 Adoption:** {nat_pct}%  ",
        f"**Underserved Market Share:** {stats.get('combined_underserved_pct', 0):.1f}%  ",
        f"**ISPs Assessed:** {stats.get('total_isps', 0)}",
        "",
        "| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |",
        "|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|",
    ]

    for isp in isps:
        lines.append(
            f"| AS{isp['asn']} "
            f"| {isp['isp'][:35]} "
            f"| {isp['market_share_pct']:.1f}% "
            f"| {isp['ipv6_prefixes']} "
            f"| {isp['cone_size']} "
            f"| {isp['ipv6_adoption_est']*100:.1f}% "
            f"| **{isp['archetype']}** — {isp['archetype_label']} "
            f"| {isp['severity']} "
            f"| +{isp['projected_impact_pp']:.1f} pp |"
        )

    lines += [
        "",
        "### Archetype Key",
        "| Code | Name | Policy Intervention |",
        "|:----:|------|---------------------|",
        "| A | Ghost (No Allocation) | Regulatory mandate for RIR membership / govt subsidy |",
        "| C | Laggard (No Traffic) | Last Mile: CPE/router hardware import standards |",
        "| D | **Bottleneck (High-Impact)** | **PRIORITY — Direct government engagement** |",
        "| OK | Compliant | No immediate intervention required |",
        "",
        "---",
        "",
        "## Section 3 — User-Side Adoption",
        "",
    ]

    # Trend table
    if trend:
        lines += [
            "### Adoption Trend",
            "",
            "| Year | IPv6 Adoption | Change |",
            "|------|:-------------:|:------:|",
        ]
        prev = None
        for t in trend:
            val  = t["adoption"]
            pct  = f"{val*100:.1f}%" if val is not None else "N/A"
            if prev is not None and val is not None:
                delta = val - prev
                chg   = f"+{delta*100:.1f} pp" if delta >= 0 else f"{delta*100:.1f} pp"
            else:
                chg = "—"
            lines.append(f"| {t['year']} | {pct} | {chg} |")
            if val is not None:
                prev = val

    # Regional comparison
    if comparison and not comparison.get("error"):
        ref   = comparison["reference"]
        g_avg = comparison["global_average_pct"]
        rank  = comparison["global_rank"]
        total = comparison["total_countries"]
        above = "above" if comparison["above_global_avg"] else "below"

        lines += [
            "",
            "### Regional Position",
            "",
            f"- **{country} adoption:** {ref['adoption_pct']}%",
            f"- **Global average:** {g_avg}%",
            f"- **Global rank:** #{rank} of {total} countries",
            f"- **vs Global Average:** {ref['adoption_pct'] - g_avg:+.1f} pp ({above} average)",
            "",
            "**Closest peer countries by adoption score:**",
            "",
            "| Country | Adoption | Gap |",
            "|---------|:--------:|:---:|",
        ]
        for p in comparison.get("closest_peers", []):
            gap = p["adoption_pct"] - ref["adoption_pct"]
            lines.append(
                f"| {p['country']} | {p['adoption_pct']}% | {gap:+.1f} pp |"
            )

    lines += [
        "",
        "---",
        "",
        "## Section 5 — Country TLD IPv6 Health",
        "",

        f"**Analyzed ccTLD:** {tld_data.get('tld', 'N/A')}  ",
        f"**Domains Sampled:** {tld_data.get('total_domains', 0)}  ",
        f"**IPv6-Enabled Domains:** {tld_data.get('ipv6_enabled_domains', 0)}  ",
        f"**IPv6 / AAAA Readiness:** {tld_data.get('percentage', 0):.2f}%  ",
        "",

        "> Sample-based analysis of the national ccTLD ecosystem",
        "> indicates the proportion of domains resolving to",
        "> IPv6-capable infrastructure.",
        "",

        "> IPv6 capability was inferred through hostname resolution",
        "> to IP nodes with address family AF=6 within the IYP graph.",
        "",
        "",

        "### Comparative TLD IPv6 Readiness",
        "",
        "| TLD | IPv6 Readiness |",
        "|------|----------------|",

        *[
            f"| {entry['tld']} | {entry['percentage']:.2f}% |"
            for entry in tld_comparison_data.get("comparisons", [])
        ],

        "",
        "> Comparative sampled analysis across major TLD ecosystems",
        "> provides relative benchmarking of IPv6 DNS readiness.",
        "---",
        "",
        "### Authoritative Nameserver IPv6 Reachability",
        "",

        f"**Nameservers Assessed:** {nameserver_data.get('total_nameservers', 0)}  ",
        f"**IPv6-Reachable Nameservers:** {nameserver_data.get('ipv6_enabled_nameservers', 0)}  ",
        f"**IPv6 NS Reachability:** {nameserver_data.get('percentage', 0):.2f}%  ",
        "",

        "> This metric measures whether authoritative DNS",
        "> infrastructure supporting the ccTLD ecosystem",
        "> is directly reachable over IPv6.",
        "",

        "> Nameserver IPv6 capability was inferred through",
        "> RESOLVES_TO relationships toward AF=6 IP nodes",
        "> within the IYP graph.",
        "",
        "---",
        "",
        "### Glue Record IPv6 Readiness",
        "",

        f"**Glue-style Nameservers Assessed:** {glue_data.get('total_glue_nameservers', 0)}  ",
        f"**IPv6-Capable Glue Nameservers:** {glue_data.get('ipv6_enabled_glue', 0)}  ",
        f"**Glue IPv6 Readiness:** {glue_data.get('percentage', 0):.2f}%  ",
        "",

        "> This approximation identifies in-zone authoritative",
        "> nameservers whose hostnames fall within the same",
        "> domain hierarchy as the delegated domain.",
        "",

        "> Results suggest that IPv6 adoption among self-hosted",
        "> authoritative DNS infrastructure remains limited",
        "> within the sampled ccTLD ecosystem.",

        "",
        "---",
        "",
        "## Impact Formula Reference",
        "",
        "```",
        "A_new = A_nat + M_z × (1.0 - A_z)",
        "",
        "  A_nat = national IPv6 adoption (0–1)",
        "  M_z   = ISP market share (0–1, from APNIC population proxy)",
        "  A_z   = ISP current IPv6 adoption estimate (0–1)",
        "```",
        "",
        "> Source: ISOC Internet Resilience Index Methodology, April 2025 v1.0",
        "> Pillar: Enabling Technologies & Security (25%) → Enabling Technologies (20%) → IPv6 (30%)",
        "",
        "---",
        "",
        f"*Report generated by ISOC Pulse × IYP IPv6 Policy Engine*  ",
        f"*Team: Rahul Rajesh, Ron Prajoth, Aditya Menon | Mentor: Amreesh Phokeer (ISOC)*",
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath