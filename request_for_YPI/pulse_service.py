import requests
from dotenv import load_dotenv
import os

# 🔥 Load environment variables
load_dotenv()

API_URL = "https://pulse-api.internetsociety.org/resilience"


def get_headers():
    api_key = os.getenv("INTERNET_SOCIETY_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Check your .env file.")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def get_data_from_year(year):
    try:
        url = f"{API_URL}?year={year}"
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def get_country_list(year):
    data = get_data_from_year(year)

    countries = set()
    for d in data.get("data", []):
        country = d.get("country")
        if country:
            countries.add(country)

    return sorted(list(countries))


def extract_all_countries_ipv6(year):
    data = get_data_from_year(year)

    results = {}

    for entry in data.get("data", []):
        country = entry.get("country")

        if not country:
            continue

        try:
            value = entry["pillars"]["security"]["dimensions"]["enabling_technologies"]["indicators"]["ipv6"]["value"]
        except KeyError:
            continue

        if value is None:
            continue

        if country not in results:
            results[country] = []

        results[country].append(value)

    final = []
    for c, vals in results.items():
        avg = sum(vals) / len(vals) if vals else None
        final.append({
            "country": c,
            "average": avg
        })

    return final


def find_similar_countries(country_code, year):
    all_data = extract_all_countries_ipv6(year)

    # 🔥 Normalize input
    country_code = country_code.upper()

    ref = next((x for x in all_data if x["country"] == country_code), None)

    if not ref or ref["average"] is None:
        return None

    ref_val = ref["average"]

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

    return distances[:5]