import json
import pathlib
import sys
from contextlib import redirect_stdout

import requests

# ============================================================
# PROJECT PATH
# ============================================================

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# ============================================================
# CONFIGURATION
# ============================================================

COUNTRY = "IN"

BASE_URL = "https://stat.ripe.net/data"

OUTPUT_FILE = (
    _ROOT
    / "testfiles"
    / "ripestat_extended_capability_output.txt"
)


# ============================================================
# GENERIC RIPEstat REQUEST
# ============================================================

def query_ripestat(endpoint, params):
    """
    Execute a RIPEstat API request and return the JSON response.
    """

    url = f"{BASE_URL}/{endpoint}/data.json"

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("URL:", response.url)
    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    return response.json()


# ============================================================
# TEST 1 — ANNOUNCED PREFIXES
# ============================================================

def test_announced_prefixes():

    print("\n" + "=" * 70)
    print("TEST 1: RIPEstat Announced Prefixes")
    print("=" * 70)

    try:

        data = query_ripestat(
            "announced-prefixes",
            {
                "resource": COUNTRY
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# TEST 2 — ASN NEIGHBOURS
# ============================================================

def test_asn_neighbours():

    print("\n" + "=" * 70)
    print("TEST 2: RIPEstat ASN Neighbours")
    print("=" * 70)

    try:

        # ASN is required for this endpoint.
        # Start with a major Indian ASN as a capability test.
        ASN = "9829"

        data = query_ripestat(
            "asn-neighbours",
            {
                "resource": ASN
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# TEST 3 — ROUTING CONSISTENCY
# ============================================================

def test_routing_consistency():

    print("\n" + "=" * 70)
    print("TEST 3: RIPEstat Routing Consistency")
    print("=" * 70)

    try:

        ASN = "9829"

        data = query_ripestat(
            "routing-consistency",
            {
                "resource": ASN
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# TEST 4 — AS PATH LENGTH
# ============================================================

def test_as_path_length():

    print("\n" + "=" * 70)
    print("TEST 4: RIPEstat AS Path Length")
    print("=" * 70)

    try:

        ASN = "9829"

        data = query_ripestat(
            "as-path-length",
            {
                "resource": ASN
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# TEST 5 — COUNTRY ASNs
# ============================================================

def test_country_asns():

    print("\n" + "=" * 70)
    print("TEST 5: RIPEstat Country ASNs")
    print("=" * 70)

    try:

        data = query_ripestat(
            "country-asns",
            {
                "resource": COUNTRY
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# TEST 6 — COUNTRY RESOURCE LIST
# ============================================================

def test_country_resource_list():

    print("\n" + "=" * 70)
    print("TEST 6: RIPEstat Country Resource List")
    print("=" * 70)

    try:

        data = query_ripestat(
            "country-resource-list",
            {
                "resource": COUNTRY
            }
        )

        print(json.dumps(data, indent=2))

        return True

    except Exception as e:

        print("ERROR:", str(e))

        return False


# ============================================================
# MAIN TEST RUNNER
# ============================================================

def main():

    print("=" * 70)
    print("RIPEstat Extended Capability Test")
    print("=" * 70)

    print("Country:", COUNTRY)
    print("Test ASN:", "9829")
    print("Output:", OUTPUT_FILE)

    print("\nStarting RIPEstat capability tests...")

    results = {}

    results["announced_prefixes"] = test_announced_prefixes()

    results["asn_neighbours"] = test_asn_neighbours()

    results["routing_consistency"] = test_routing_consistency()

    results["as_path_length"] = test_as_path_length()

    results["country_asns"] = test_country_asns()

    results["country_resource_list"] = test_country_resource_list()


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    successful = 0
    failed = 0

    for test_name, success in results.items():

        status = "SUCCESS" if success else "FAILED"

        print(f"{test_name:30} {status}")

        if success:
            successful += 1
        else:
            failed += 1

    print("\nTotal tests:", len(results))
    print("Successful:", successful)
    print("Failed:", failed)

    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)


# ============================================================
# SAVE EVERYTHING TO TXT
# ============================================================

if __name__ == "__main__":

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f, redirect_stdout(f):

        main()

    print("RIPEstat extended test completed.")
    print(f"Output saved to: {OUTPUT_FILE}")