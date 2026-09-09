import json
from contextlib import redirect_stdout

import requests

COUNTRY = "India"
PCH_URL = "https://www.pch.net/api/ixp/directory/Active"

OUTPUT_FILE = "testfiles/ixp_traffic_test_output.txt"


def bytes_to_gbps(value):
    """
    Convert bits-per-second to Gbps.
    """
    if value is None:
        return None

    return round(float(value) / 1_000_000_000, 3)


def run_test():

    print("=" * 70)
    print("2.3 — AGGREGATED IXP TRAFFIC TEST")
    print("=" * 70)

    print(f"Country: {COUNTRY}")
    print(f"PCH API: {PCH_URL}")
    print()

    try:

        response = requests.get(
            PCH_URL,
            timeout=30
        )

        print("HTTP Status:", response.status_code)
        print("URL:", response.url)
        print()

        response.raise_for_status()

        payload = response.json()

        # ---------------------------------------------------------
        # Validate response
        # ---------------------------------------------------------

        if not isinstance(payload, list):

            print("ERROR: Unexpected PCH response format")
            print("Response type:", type(payload))

            print()
            print("RAW RESPONSE:")
            print(json.dumps(payload, indent=2))

            return

        # ---------------------------------------------------------
        # Find Indian IXPs
        # ---------------------------------------------------------

        india_ixps = [
            ixp
            for ixp in payload
            if str(ixp.get("ctry", "")).strip().lower()
            == COUNTRY.lower()
        ]

        print(f"Total active PCH records: {len(payload)}")
        print(f"India IXPs found: {len(india_ixps)}")
        print()

        if not india_ixps:

            print("No India IXPs found in PCH.")
            return

        # ---------------------------------------------------------
        # Traffic aggregation
        # ---------------------------------------------------------

        total_peak = 0.0
        total_average = 0.0

        peak_count = 0
        average_count = 0

        # Keep individual IXP results
        ixp_results = []

        # ---------------------------------------------------------
        # Individual IXP records
        # ---------------------------------------------------------

        print("=" * 70)
        print("INDIA IXP TRAFFIC RECORDS")
        print("=" * 70)

        for ixp in india_ixps:

            name = ixp.get("name")
            city = ixp.get("cit")
            ixp_id = ixp.get("id")
            status = ixp.get("stat")

            peak_raw = ixp.get("traf")
            average_raw = ixp.get("avg")

            # Convert values safely
            try:
                peak = float(peak_raw)
            except (TypeError, ValueError):
                peak = 0.0

            try:
                average = float(average_raw)
            except (TypeError, ValueError):
                average = 0.0

            # Aggregate
            if peak > 0:
                total_peak += peak
                peak_count += 1

            if average > 0:
                total_average += average
                average_count += 1

            peak_gbps = bytes_to_gbps(peak)
            average_gbps = bytes_to_gbps(average)

            ixp_results.append({
                "id": ixp_id,
                "name": name,
                "city": city,
                "status": status,
                "peak_raw": peak_raw,
                "average_raw": average_raw,
                "peak_traffic_gbps": peak_gbps,
                "average_traffic_gbps": average_gbps,
                "updated": ixp.get("updt")
            })

            print(f"IXP: {name}")
            print(f"City: {city}")
            print(f"PCH ID: {ixp_id}")
            print(f"Status: {status}")

            print()
            print(f"Peak raw: {peak_raw}")
            print(f"Average raw: {average_raw}")

            print()
            print(f"Peak traffic: {peak_gbps:.3f} Gbps")
            print(f"Average traffic: {average_gbps:.3f} Gbps")

            print("-" * 70)

        # ---------------------------------------------------------
        # Aggregated result
        # ---------------------------------------------------------

        total_peak_gbps = bytes_to_gbps(total_peak)
        total_average_gbps = bytes_to_gbps(total_average)

        print()
        print("=" * 70)
        print("AGGREGATED INDIA IXP TRAFFIC")
        print("=" * 70)

        print(f"IXPs found: {len(india_ixps)}")
        print(f"IXPs with peak traffic data: {peak_count}")
        print(f"IXPs with average traffic data: {average_count}")

        print()
        print(
            f"TOTAL PEAK TRAFFIC: "
            f"{total_peak_gbps:.3f} Gbps"
        )

        print(
            f"TOTAL AVERAGE TRAFFIC: "
            f"{total_average_gbps:.3f} Gbps"
        )

        # ---------------------------------------------------------
        # Interpretation
        # ---------------------------------------------------------

        print()
        print("=" * 70)
        print("2.3 METRIC SUMMARY")
        print("=" * 70)

        print("Metric: Aggregated IXP Traffic")
        print(f"Country: {COUNTRY}")

        print()
        print(f"Peak traffic: {total_peak_gbps:.3f} Gbps")
        print(f"Average traffic: {total_average_gbps:.3f} Gbps")

        print()
        print("Source: PCH")
        print(
            "Method: Sum of PCH-reported peak and average "
            "IPv4 traffic across Indian IXPs"
        )

        print()
        print(
            "NOTE: PCH traffic values represent reported IPv4 "
            "traffic and may not cover every IXP listed by PeeringDB."
        )

        # ---------------------------------------------------------
        # Raw data
        # ---------------------------------------------------------

        print()
        print("=" * 70)
        print("RAW INDIA IXP RECORDS")
        print("=" * 70)

        print(json.dumps(india_ixps, indent=2))

        # ---------------------------------------------------------
        # Processed JSON summary
        # ---------------------------------------------------------

        print()
        print("=" * 70)
        print("PROCESSED TRAFFIC SUMMARY")
        print("=" * 70)

        summary = {
            "metric": "aggregated_ixp_traffic",
            "country": COUNTRY,
            "peak_traffic_gbps": total_peak_gbps,
            "average_traffic_gbps": total_average_gbps,
            "ixp_count": len(india_ixps),
            "ixps_with_peak_data": peak_count,
            "ixps_with_average_data": average_count,
            "source": "PCH",
            "method": (
                "Sum of PCH-reported peak and average IPv4 "
                "traffic across domestic IXPs"
            ),
            "status": "measured",
            "ixps": ixp_results
        }

        print(json.dumps(summary, indent=2))

    except requests.RequestException as e:

        print("REQUEST ERROR:")
        print(type(e).__name__, e)

    except Exception as e:

        print("ERROR:")
        print(type(e).__name__, e)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as output, redirect_stdout(output):
        run_test()

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print(f"Output saved to: {OUTPUT_FILE}")