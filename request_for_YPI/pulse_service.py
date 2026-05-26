import requests
from dotenv import load_dotenv
import os

# 🔥 NEW: Neo4j execution import
from request_for_YPI.src.request_IYP.request_testing import execute_cypher_test

# Load environment variables
load_dotenv()

API_URL = "https://pulse-api.internetsociety.org/resilience"


# =========================
# 🔑 AUTH
# =========================
def get_headers():
    api_key = os.getenv("INTERNET_SOCIETY_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Check your .env file.")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


# =========================
# 🌐 FETCH DATA
# =========================
def get_data_from_year(year):
    try:
        url = f"{API_URL}?year={year}"
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


# =========================
# 🌍 COUNTRY LIST
# =========================
def get_country_list(year):
    data = get_data_from_year(year)

    countries = set()
    for d in data.get("data", []):
        country = d.get("country")
        if country:
            countries.add(country)

    return sorted(list(countries))


# =========================
# 📊 INDICATOR EXTRACTION
# =========================
def get_indicator_value(entry, indicator):
    try:
        dims = entry["pillars"]["security"]["dimensions"]

        for dim in dims.values():
            indicators = dim.get("indicators", {})

            for key, val in indicators.items():

                # Exact indicator match only
                if indicator == key:
                    return val.get("value")

        return None

    except Exception:
        return None


def extract_all_countries_indicator(year, indicator):
    data = get_data_from_year(year)

    results = {}

    for entry in data.get("data", []):
        country = entry.get("country")
        
        if not country:
            continue

        value = get_indicator_value(entry, indicator)

        if value is None:
            continue

        if country not in results:
            results[country] = []

        results[country].append(value)

    final = []
    for c, vals in results.items():
        avg = sum(vals) / len(vals) if vals else None

        if avg is not None:
            final.append({
                "country": c,
                "average": avg
            })

    return final


# =========================
# 🔍 SIMILARITY ENGINE
# =========================
def find_similar_countries(country_code, year, indicator="ipv6"):
    all_data = extract_all_countries_indicator(year, indicator)

    country_code = country_code.upper()

    ref = next((x for x in all_data if x["country"] == country_code), None)

    if not ref or ref["average"] is None:
        return {
            "error": f"No data available for {country_code} in {indicator}"
        }

    ref_val = ref["average"]

    # 🔥 Detect binary indicator
    unique_values = set([x["average"] for x in all_data])

    if unique_values.issubset({0.0, 1.0}):
        # ✅ BINARY MODE
        same = []
        different = []

        for c in all_data:
            if c["country"] == country_code:
                continue

            if c["average"] == ref_val:
                same.append(c)
            else:
                different.append(c)

        return {
            "type": "binary",
            "reference": {
                "country": country_code,
                "average": ref_val
            },
            "same_group": same,
            "different_group": different
        }

    else:
        # ✅ CONTINUOUS MODE
        distances = []

        for c in all_data:
            if c["country"] == country_code or c["average"] is None:
                continue

            dist = abs(c["average"] - ref_val)

            distances.append({
                "country": c["country"],
                "average": c["average"],
                "distance": dist
            })

        distances.sort(key=lambda x: x["distance"])

        return {
            "type": "continuous",
            "reference": {
                "country": country_code,
                "average": ref_val
            },
            "similar": distances[:5]
        }


# =========================
# 🧠 ASN + ISP DATA (ENHANCED)
# =========================
def get_asn_by_country(country_code):
    # 1. Get country IPv6 baseline
    ipv6_data = extract_all_countries_indicator(2024, "ipv6")
    country_ipv6 = next(
        (x["average"] for x in ipv6_data if x["country"] == country_code),
        None
    )

    if country_ipv6 is None:
        return {"error": "No IPv6 data found for country"}

    # 2. ASN query (fixed + deduplicated)
    query = f"""
    MATCH (a:AS)-[r:POPULATION]->(c:Country {{country_code: '{country_code}'}})
    OPTIONAL MATCH (a)-[:NAME]->(n:Name)
    WITH 
        a.asn AS asn,
        collect(DISTINCT n.name)[0] AS isp,
        r.percent AS market_share
    RETURN asn, isp, market_share
    ORDER BY market_share DESC
    LIMIT 20
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {"error": result["error"]}

    # 3. 🔥 Smarter IPv6 estimation + classification
    enriched = []

    for row in result["data"]:
        share = row["market_share"]

        # Normalize share (0–1 scale)
        normalized = share / 100  

        # Center around 0 (range: -0.5 to +0.5)
        centered = normalized - 0.5  

        # Scale influence
        adjustment = centered * 0.4   # +/- 40%

        ipv6_estimate = max(0.0, min(1.0, country_ipv6 * (1 + adjustment)))

        # 🔥 Classification
        if ipv6_estimate >= 0.7:
            category = "High"
        elif ipv6_estimate >= 0.4:
            category = "Medium"
        else:
            category = "Low"

        enriched.append({
            "asn": row["asn"],
            "isp": row["isp"],
            "market_share": share,
            "ipv6_estimate": round(ipv6_estimate, 4),
            "category": category
        })

    return enriched

# =========================
# 🚨 IPv6 GAPS (NO IPv6 SUPPORT)
# =========================
def get_ipv6_gaps(country_code):

    query = f"""
    MATCH (c:Country {{country_code: '{country_code}'}})<-[:COUNTRY]-(as:AS)

    OPTIONAL MATCH (as)-[:ORIGINATE]->(p:Prefix)
    WHERE p.prefix CONTAINS ':'

    WITH as, count(p) AS ipv6PrefixCount

    WHERE ipv6PrefixCount = 0

    MATCH (as)-[r:RANK]->(rank:Ranking {{name:'CAIDA ASRank'}})

    OPTIONAL MATCH (as)-[:NAME]->(n:Name)

    RETURN
        as.asn AS asn,
        collect(DISTINCT n.name)[0] AS isp,
        r['cone:numberAsns'] AS customerConeSize
    ORDER BY customerConeSize DESC
    LIMIT 15
    """

    result = execute_cypher_test(query)

    if not result["success"]:
        return {"error": result["error"]}

    # 🔥 Add severity classification
    enriched = []

    for row in result["data"]:

        cone = row.get("customerConeSize") or 0

        if cone >= 1000:
            severity = "Critical"
        elif cone >= 200:
            severity = "High"
        elif cone >= 50:
            severity = "Medium"
        else:
            severity = "Low"

        enriched.append({
            "asn": row["asn"],
            "isp": row["isp"] or "(Unnamed)",
            "customerConeSize": cone,
            "severity": severity
        })

    return enriched