from collections import Counter

import requests

BASE_URL = "https://www.peeringdb.com/api"


def get_ixps(country="IN"):
    response = requests.get(
        f"{BASE_URL}/ix",
        params={
            "country": country,
            "limit": 200,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json().get("data", [])


print("=" * 70)
print("PEERINGDB IXP ANALYSIS")
print("=" * 70)

try:
    ixps = get_ixps("IN")

    print(f"Total IXP records: {len(ixps)}")
    print()

    # ---------------------------------------------------------
    # 2.1 — Operational / participation proxy
    # ---------------------------------------------------------

    operational = [
        ixp for ixp in ixps
        if ixp.get("status") == "ok"
    ]

    with_networks = [
        ixp for ixp in operational
        if (ixp.get("net_count") or 0) > 0
    ]

    without_networks = [
        ixp for ixp in operational
        if (ixp.get("net_count") or 0) == 0
    ]

    print("=" * 70)
    print("2.1 — IXP OPERATIONAL / PARTICIPATION STATUS")
    print("=" * 70)

    print(f"Total IXPs: {len(ixps)}")
    print(f"Status OK: {len(operational)}")
    print(f"With listed networks: {len(with_networks)}")
    print(f"Without listed networks: {len(without_networks)}")
    print()

    for ixp in ixps:
        print(
            f"{ixp.get('name')} | "
            f"City: {ixp.get('city')} | "
            f"Networks: {ixp.get('net_count')} | "
            f"Facilities: {ixp.get('fac_count')} | "
            f"Status: {ixp.get('status')}"
        )

    # ---------------------------------------------------------
    # 2.2 — Geographic distribution
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("2.2 — GEOGRAPHIC DISTRIBUTION")
    print("=" * 70)

    city_counts = Counter(
        ixp.get("city") or "Unknown"
        for ixp in ixps
    )

    print(f"Unique cities: {len(city_counts)}")
    print()

    for city, count in city_counts.most_common():
        percentage = (count / len(ixps)) * 100

        print(
            f"{city}: "
            f"{count} IXPs "
            f"({percentage:.2f}%)"
        )

except Exception as e:
    print("ERROR:")
    print(e)