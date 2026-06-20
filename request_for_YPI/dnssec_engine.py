"""
dnssec_engine.py
================

DNSSEC Policy Engine
ISOC Pulse × IYP

Currently implemented:

Section 1.2   - Number of authoritative nameservers
Section 1.2.1 - IPv6 enablement of authoritative nameservers
Section 1.2.2 - ASN diversity of authoritative nameservers

Authors:
Rahul Rajesh
Ron Prajoth
Aditya Menon

Mentor:
Amreesh Phokeer
"""

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from request_for_YPI.src.request_IYP.request_testing import execute_cypher_test


# ============================================================
# SECTION 1.2
# Number of authoritative nameservers
# ============================================================

def get_ccTLD_nameserver_count(country_code: str) -> dict:

    country_code = country_code.lower()

    query = f"""
    MATCH (d:DomainName {{name:'{country_code}'}})
          -[:MANAGED_BY]->(ns:AuthoritativeNameServer)

    RETURN
        count(DISTINCT ns) AS nameserverCount
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {"error": result["error"]}

    row = result["data"][0]

    return {
        "country": country_code.upper(),
        "nameserver_count": row["nameserverCount"],
        "error": None
    }


# ============================================================
# SECTION 1.2.1
# IPv6 Enablement
# ============================================================

def get_ccTLD_ipv6_enablement(country_code: str) -> dict:

    country_code = country_code.lower()

    query = f"""
    MATCH (d:DomainName {{name:'{country_code}'}})
          -[:MANAGED_BY]->(ns:AuthoritativeNameServer)
          -[:RESOLVES_TO]->(ip:IP)

    RETURN
        ns.name AS nameserver,
        collect(DISTINCT ip.af) AS addressFamilies
    ORDER BY nameserver
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {"error": result["error"]}

    nameservers = []

    ipv6_enabled = 0

    for row in result["data"]:

        families = row["addressFamilies"]

        has_ipv6 = 6 in families

        if has_ipv6:
            ipv6_enabled += 1

        nameservers.append({
            "nameserver": row["nameserver"],
            "address_families": families,
            "ipv6_enabled": has_ipv6
        })

    total = len(nameservers)

    percentage = (
        round((ipv6_enabled / total) * 100, 2)
        if total > 0 else 0
    )

    return {
        "country": country_code.upper(),
        "total_nameservers": total,
        "ipv6_enabled_nameservers": ipv6_enabled,
        "ipv6_percentage": percentage,
        "nameservers": nameservers,
        "error": None
    }


# ============================================================
# SECTION 1.2.2
# ASN Diversity
# ============================================================

def get_ccTLD_asn_diversity(country_code: str) -> dict:

    country_code = country_code.lower()

    query = f"""
    MATCH (d:DomainName {{name:'{country_code}'}})
          -[:MANAGED_BY]->(ns:AuthoritativeNameServer)
          -[:RESOLVES_TO]->(ip:IP)
          -[:PART_OF]->(p:BGPPrefix)
    <-[:ORIGINATE]-(a:AS)

    RETURN DISTINCT
        ns.name AS nameserver,
        a.asn AS asn,
        ip.ip AS ip
    ORDER BY nameserver
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {"error": result["error"]}

    records = result["data"]

    asns = sorted(
        list(
            set(
                row["asn"]
                for row in records
            )
        )
    )

    return {
        "country": country_code.upper(),
        "distinct_asns": len(asns),
        "asns": asns,
        "records": records,
        "error": None
    }