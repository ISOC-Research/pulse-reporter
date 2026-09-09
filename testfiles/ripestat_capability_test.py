import json
import pathlib
import sys
from contextlib import redirect_stdout

import requests

# Project root
_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

COUNTRY = "IN"

# Output file
OUTPUT_FILE = _ROOT / "testfiles" / "ripestat_capability_output.txt"


def test_country_asns():
    print("\n" + "=" * 70)
    print("TEST: RIPEstat Country ASNs")
    print("=" * 70)

    url = "https://stat.ripe.net/data/country-asns/data.json"

    params = {
        "resource": COUNTRY
    }

    response = requests.get(url, params=params, timeout=30)

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print(json.dumps(data, indent=2))


def test_country_resource_list():
    print("\n" + "=" * 70)
    print("TEST: RIPEstat Country Resource List")
    print("=" * 70)

    url = "https://stat.ripe.net/data/country-resource-list/data.json"

    params = {
        "resource": COUNTRY
    }

    response = requests.get(url, params=params, timeout=30)

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print(json.dumps(data, indent=2))


def main():
    print("=" * 70)
    print("RIPEstat Capability Test")
    print("=" * 70)
    print("Country:", COUNTRY)
    print("Output:", OUTPUT_FILE)

    test_country_asns()
    test_country_resource_list()

    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f, redirect_stdout(f):
        main()

    print("RIPEstat test completed.")
    print(f"Output saved to: {OUTPUT_FILE}")