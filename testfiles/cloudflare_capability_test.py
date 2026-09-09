import json
import pathlib
import sys
from contextlib import redirect_stdout

# ============================================================
# PROJECT PATH
# ============================================================

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if str(_ROOT / "request_for_YPI") not in sys.path:
    sys.path.insert(0, str(_ROOT / "request_for_YPI"))


# ============================================================
# CLOUDFLARE RADAR
# ============================================================

try:
    from request_for_YPI.src.tools.cloudflare_radar import RadarClient
except Exception as e:
    print("❌ Could not import RadarClient")
    print(e)
    sys.exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

COUNTRY = "IN"
DATE_RANGE = "90d"

OUTPUT_FILE = _ROOT / "testfiles" / "cloudflare_capability_output.txt"

client = RadarClient()


# ============================================================
# HELPER
# ============================================================

def test_metric(name, function, *args, **kwargs):

    print("\n" + "=" * 70)
    print(f"🔎 TESTING: {name}")
    print("=" * 70)

    try:

        result = function(*args, **kwargs)

        if result is None:
            print("⚠️ API returned None")
            return

        print("✅ API CALL SUCCEEDED")

        print("\n📦 RAW RESPONSE:")
        print(json.dumps(result, indent=2, default=str))

    except Exception as e:

        print("❌ API CALL FAILED")
        print(f"Error type: {type(e).__name__}")
        print(f"Error: {e}")


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_tests():

    print("=" * 70)
    print("CLOUDFLARE RADAR CAPABILITY TEST")
    print(f"Country: {COUNTRY}")
    print(f"Date Range: {DATE_RANGE}")
    print("=" * 70)

    # 1. Internet Speed
    test_metric(
        "Speed Summary",
        client.get_speed_summary,
        COUNTRY,
        DATE_RANGE
    )

    # 2. IQI - Bandwidth
    test_metric(
        "IQI - Bandwidth",
        client.get_iqi_summary,
        COUNTRY,
        "bandwidth",
        DATE_RANGE
    )

    # 3. IQI - Latency
    test_metric(
        "IQI - Latency",
        client.get_iqi_summary,
        COUNTRY,
        "latency",
        DATE_RANGE
    )

    # 4. IQI - DNS
    test_metric(
        "IQI - DNS",
        client.get_iqi_summary,
        COUNTRY,
        "dns",
        DATE_RANGE
    )

    # 5. Speed Histogram
    test_metric(
        "Speed Histogram",
        client.get_speed_histogram,
        COUNTRY,
        "downloadSpeed",
        DATE_RANGE
    )

    # 6. TCP Resets / Timeouts
    test_metric(
        "TCP Resets / Timeouts",
        client.get_tcp_resets_timeouts_summary,
        COUNTRY,
        DATE_RANGE
    )

    # 7. Traffic Anomalies
    test_metric(
        "Traffic Anomalies",
        client.get_traffic_anomalies,
        COUNTRY,
        DATE_RANGE
    )

    print("\n")
    print("=" * 70)
    print("🏁 CLOUDFLARE RADAR CAPABILITY TEST COMPLETE")
    print("=" * 70)


# ============================================================
# SAVE EVERYTHING TO TXT
# ============================================================

print("\n📄 Saving output to:")
print(OUTPUT_FILE)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f, redirect_stdout(f):
    run_tests()

print("✅ Test complete.")
print(f"📄 Output saved to: {OUTPUT_FILE}")