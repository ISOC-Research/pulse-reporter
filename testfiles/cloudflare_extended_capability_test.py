import json
import pathlib
import sys
from contextlib import redirect_stdout

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from request_for_YPI.src.tools.cloudflare_radar import RadarClient

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

COUNTRY = "IN"
DATE_RANGE = "90d"

OUTPUT_FILE = (
    _ROOT
    / "testfiles"
    / "cloudflare_extended_capability_output.txt"
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def print_result(name, result):
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    print(json.dumps(result, indent=2, ensure_ascii=False))


def run_test(name, function):
    print("\n" + "#" * 80)
    print(f"TEST: {name}")
    print("#" * 80)

    try:
        result = function()

        print("STATUS: SUCCESS")
        print_result(name, result)

        return {
            "name": name,
            "status": "SUCCESS",
            "result": result,
            "error": None,
        }

    except Exception as e:
        print("STATUS: FAILED")
        print(f"ERROR: {type(e).__name__}: {e}")

        return {
            "name": name,
            "status": "FAILED",
            "result": None,
            "error": str(e),
        }


# ---------------------------------------------------------
# Main test suite
# ---------------------------------------------------------

def run_tests():

    print("=" * 80)
    print("CLOUDFLARE RADAR EXTENDED CAPABILITY TEST")
    print("=" * 80)

    print(f"Country: {COUNTRY}")
    print(f"Date Range: {DATE_RANGE}")

    client = RadarClient()

    results = []

    # =====================================================
    # 1. SPEED TOP LOCATIONS
    # =====================================================

    print("\n\n")
    print("=" * 80)
    print("1. SPEED TOP LOCATIONS")
    print("=" * 80)

    speed_metrics = [
        "downloadSpeed",
        "uploadSpeed",
        "jitter",
        "latency",
    ]

    for metric in speed_metrics:

        results.append(
            run_test(
                f"Speed Top Locations - {metric}",
                lambda metric=metric:
                    client.get_speed_top_locations(
                        metric=metric,
                        date_range=DATE_RANGE,
                        limit=10,
                    ),
            )
        )

    # =====================================================
    # 2. IQI TIMESERIES
    # =====================================================

    print("\n\n")
    print("=" * 80)
    print("2. INTERNET QUALITY INDEX TIMESERIES")
    print("=" * 80)

    iqi_metrics = [
        "bandwidth",
        "latency",
        "dns",
    ]

    for metric in iqi_metrics:

        results.append(
            run_test(
                f"IQI Timeseries - {metric}",
                lambda metric=metric:
                    client.get_iqi_timeseries(
                        country=COUNTRY,
                        metric=metric,
                        date_range=DATE_RANGE,
                    ),
            )
        )

    # =====================================================
    # 3. SPEED HISTOGRAM - ADDITIONAL METRICS
    # =====================================================

    print("\n\n")
    print("=" * 80)
    print("3. SPEED HISTOGRAM - ALL METRICS")
    print("=" * 80)

    histogram_metrics = [
        "downloadSpeed",
        "uploadSpeed",
        "latency",
        "jitter",
    ]

    for metric in histogram_metrics:

        results.append(
            run_test(
                f"Speed Histogram - {metric}",
                lambda metric=metric:
                    client.get_speed_histogram(
                        country=COUNTRY,
                        metric=metric,
                        bucket_count=10,
                        date_range=DATE_RANGE,
                    ),
            )
        )

    # =====================================================
    # 4. SUMMARY
    # =====================================================

    print("\n\n")
    print("=" * 80)
    print("EXTENDED CAPABILITY TEST SUMMARY")
    print("=" * 80)

    successful = 0
    failed = 0

    for item in results:

        if item["status"] == "SUCCESS":
            successful += 1
            symbol = "SUCCESS"
        else:
            failed += 1
            symbol = "FAILED"

        print(f"[{symbol}] {item['name']}")

    print("\n" + "-" * 80)

    print(f"Total tests : {len(results)}")
    print(f"Successful  : {successful}")
    print(f"Failed      : {failed}")

    print("-" * 80)

    # -----------------------------------------------------
    # Capability interpretation
    # -----------------------------------------------------

    print("\n")
    print("=" * 80)
    print("PEERING MODULE RELEVANCE")
    print("=" * 80)

    print("""
The following Cloudflare Radar capabilities may be useful
for the Peering indicator:

1. Speed summary
   - Country-level download/upload performance
   - Latency
   - Jitter
   - Packet loss

2. IQI summary
   - Bandwidth percentiles
   - Latency percentiles
   - DNS latency percentiles

3. IQI timeseries
   - Useful for detecting trends over time
   - Can potentially show degradation/improvement

4. Speed histogram
   - Useful for understanding distribution/inequality
   - Can show whether performance is concentrated
     around a narrow or wide range

5. Speed top locations
   - Can provide geographic comparison/ranking
   - Useful only if the returned locations can be
     meaningfully mapped to domestic geography

6. TCP resets/timeouts
   - Useful as a network reliability/stability signal

7. Traffic anomalies
   - Potentially useful for identifying instability,
     but requires careful interpretation
""")

    print("\n")
    print("=" * 80)
    print("END OF TEST")
    print("=" * 80)


# ---------------------------------------------------------
# Save output to TXT
# ---------------------------------------------------------

if __name__ == "__main__":

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f, redirect_stdout(f):
        run_tests()

    print(
        f"\nCloudflare extended capability test complete.\n"
        f"Output saved to:\n{OUTPUT_FILE}"
    )