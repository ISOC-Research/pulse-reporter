import requests
from dotenv import load_dotenv
import os

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

        # 🔥 Search ALL dimensions dynamically
        for dim in dims.values():
            indicators = dim.get("indicators", {})

            for key, val in indicators.items():
                if indicator in key:   # match "dnssec"
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