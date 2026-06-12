"""
APNIC IPv6 Adoption Service
============================
Fetches real IPv6 adoption data directly from APNIC Labs
(stats.labs.apnic.net) as recommended by Amreesh.

This replaces the ISOC Pulse API for user-side adoption metrics,
which was returning anomalous data (e.g., 100% for India).

No API key required — APNIC data is completely public.
"""

import requests
import re
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════

def get_apnic_country_adoption(country_code: str) -> dict:
    """
    Get the latest IPv6 adoption rate for a single country from APNIC.
    
    Returns:
        dict with keys: country_code, adoption_pct, source, date, error
    """
    all_data = _fetch_all_country_data()
    if all_data.get("error"):
        return {"error": all_data["error"]}
    
    cc = country_code.upper()
    countries = all_data["countries"]
    
    if cc not in countries:
        return {"error": f"Country code '{cc}' not found in APNIC data."}
    
    return {
        "country_code": cc,
        "adoption_pct": countries[cc],
        "source": "APNIC Labs IPv6 Measurement",
        "date": all_data["date"],
        "error": None
    }


def get_apnic_global_ranking(country_code: str) -> dict:
    """
    Get the global ranking + peer comparison for a country.
    
    Returns:
        dict with: rank, total_countries, adoption_pct, global_avg,
                   top_peers (list of nearby countries), error
    """
    all_data = _fetch_all_country_data()
    if all_data.get("error"):
        return {"error": all_data["error"]}
    
    cc = country_code.upper()
    countries = all_data["countries"]
    
    if cc not in countries:
        return {"error": f"Country code '{cc}' not found in APNIC data."}
    
    # Sort all countries by adoption descending
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    
    # Find rank
    rank = None
    for i, (code, pct) in enumerate(sorted_countries):
        if code == cc:
            rank = i + 1
            break
    
    # Global average
    all_values = [v for v in countries.values() if v > 0]
    global_avg = round(sum(all_values) / len(all_values), 2) if all_values else 0.0
    
    # Find closest peers (countries within +/- 10pp)
    target = countries[cc]
    peers = []
    for code, pct in sorted_countries:
        if code != cc and abs(pct - target) <= 10:
            peers.append({"country": code, "adoption": pct, "gap": round(pct - target, 1)})
    # Take top 5 closest
    peers.sort(key=lambda x: abs(x["gap"]))
    peers = peers[:5]
    
    return {
        "country_code": cc,
        "adoption_pct": countries[cc],
        "rank": rank,
        "total_countries": len(sorted_countries),
        "global_avg": global_avg,
        "peers": peers,
        "source": "APNIC Labs IPv6 Measurement",
        "date": all_data["date"],
        "error": None
    }


def get_apnic_asn_adoption(asn: int) -> dict:
    """
    Get IPv6 adoption for a specific ASN from APNIC.
    Scrapes the per-ASN page at stats.labs.apnic.net/ipv6/AS{asn}
    
    Returns:
        dict with: asn, adoption_pct, samples, source, error
    """
    url = f"https://stats.labs.apnic.net/ipv6/AS{asn}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {"error": f"APNIC returned status {resp.status_code} for AS{asn}"}
        
        # The page embeds data in JavaScript like:
        # ['2026-06-10', 78.42, 12345, ...]
        # We look for the most recent data point
        html = resp.text
        
        # Try to find the preferred percentage in the page
        # Pattern: data.addRows([ ... ['date', capable, preferred, ...] ... ])
        # Simpler: look for the summary stats displayed on the page
        match = re.search(r"IPv6 Capable[^0-9]*?([0-9.]+)%", html)
        if match:
            adoption = float(match.group(1))
            return {
                "asn": asn,
                "adoption_pct": adoption,
                "source": "APNIC Labs IPv6 Measurement",
                "error": None
            }
        
        return {"error": f"Could not parse adoption data for AS{asn}"}
        
    except Exception as e:
        return {"error": f"APNIC request failed for AS{asn}: {str(e)}"}


# ═══════════════════════════════════════════════════════════════
# INTERNAL — Data Fetching & Parsing
# ═══════════════════════════════════════════════════════════════

_CACHE = {}  # Simple in-memory cache to avoid re-fetching in same run

def _fetch_all_country_data() -> dict:
    """
    Scrape the APNIC IPv6 world map page and extract all country
    adoption percentages from the embedded JavaScript.
    
    The page contains data like:
        ['FR', {v: 83.79, f:'83.79%'}],
        ['IN', {v: 78.42, f:'78.42%'}],
    
    Returns:
        dict with: countries (dict of CC -> pct), date, error
    """
    cache_key = "all_countries"
    if cache_key in _CACHE:
        return _CACHE[cache_key]
    
    url = "https://stats.labs.apnic.net/ipv6"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {"error": f"APNIC returned status {resp.status_code}"}
        
        html = resp.text
        
        # Parse: ['CC', {v: 83.79, f:'83.79%'}],
        pattern = r"\['([A-Z]{2})',\s*\{v:\s*([\d.]+)"
        matches = re.findall(pattern, html)
        
        if not matches:
            return {"error": "Could not parse country data from APNIC page."}
        
        countries = {}
        for cc, pct in matches:
            countries[cc] = float(pct)
        
        result = {
            "countries": countries,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": len(countries),
            "error": None
        }
        
        _CACHE[cache_key] = result
        return result
        
    except Exception as e:
        return {"error": f"APNIC request failed: {str(e)}"}


# ═══════════════════════════════════════════════════════════════
# CLI TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    cc = sys.argv[1].upper() if len(sys.argv) > 1 else "FR"
    
    print(f"═══ APNIC IPv6 Data for {cc} ═══\n")
    
    # Test 1: Country adoption
    result = get_apnic_country_adoption(cc)
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ {cc} IPv6 Adoption: {result['adoption_pct']}%")
        print(f"   Source: {result['source']}")
        print(f"   Date: {result['date']}")
    
    print()
    
    # Test 2: Global ranking
    ranking = get_apnic_global_ranking(cc)
    if ranking.get("error"):
        print(f"❌ Ranking Error: {ranking['error']}")
    else:
        print(f"📊 Global Rank: #{ranking['rank']} of {ranking['total_countries']} countries")
        print(f"   Global Average: {ranking['global_avg']}%")
        print(f"   Gap vs Global: {round(ranking['adoption_pct'] - ranking['global_avg'], 1):+} pp")
        print(f"\n   Closest Peers:")
        for p in ranking['peers']:
            print(f"     {p['country']}: {p['adoption']}% ({p['gap']:+} pp)")
