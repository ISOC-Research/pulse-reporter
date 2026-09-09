import json

import requests

URL = "https://stat.ripe.net/data/country-asns/data.json"

params = {
    "resource": "IN"
}

response = requests.get(
    URL,
    params=params,
    timeout=30
)

print("HTTP Status:", response.status_code)
print("URL:", response.url)
print()

data = response.json()

print("TOP LEVEL KEYS:")
print(data.keys())
print()

print("FULL RESPONSE:")
print(json.dumps(data, indent=2))