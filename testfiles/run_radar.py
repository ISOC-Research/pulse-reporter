"""
Cloudflare Radar Performance Runner
=====================================
Fetches internet quality/speed data from the Cloudflare Radar API for a given
country and formats the output for LLM consumption — mirroring how run_query.py
works for Cypher/Neo4j queries.

Usage:
    python testfiles/run_radar.py --country AU
    python testfiles/run_radar.py --country FR --metric latency
    python testfiles/run_radar.py --country SN --date-range 30d
"""

import argparse
import io
import json
import os
import sys

# Force UTF-8 output for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'request_for_YPI'))

from request_for_YPI.src.tools.cloudflare_radar import RadarClient


def format_speed_summary(result: dict, country: str) -> str:
    """Format speed test summary into readable output."""
    summary = result.get("summary_0", {})
    meta = result.get("meta", {})

    download = summary.get("downloadSpeed", "N/A")
    upload = summary.get("uploadSpeed", "N/A")
    latency = summary.get("latencyIdle", summary.get("latency", "N/A"))
    jitter = summary.get("jitterIdle", summary.get("jitter", "N/A"))

    date_range = meta.get("dateRange", [{}])
    start = date_range[0].get("startTime", "N/A") if date_range else "N/A"
    end = date_range[0].get("endTime", "N/A") if date_range else "N/A"

    confidence = meta.get("confidenceInfo", {}).get("level", "N/A")

    lines = [
        f"Title: Internet Speed Performance in {country.upper()}",
        "",
        "This data is sourced from the Cloudflare Radar API, aggregated from speed",
        "tests run by real users on speed.cloudflare.com. It provides a near-real-time",
        "view of internet performance — updated continuously, not quarterly like Ookla.",
        "",
        f"**Measurement Period:** {start} to {end}",
        f"**Confidence Level:** {confidence}",
        "",
        "**Speed Test Results:**",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Download Speed | {download} Mbps |",
        f"| Upload Speed | {upload} Mbps |",
        f"| Latency (idle) | {latency} ms |",
        f"| Jitter (idle) | {jitter} ms |",
        "",
        "**Interpretation:**",
        "",
        f"Download speed of {download} Mbps and upload speed of {upload} Mbps",
        f"represent the median connection quality in {country.upper()}. Latency of",
        f"{latency} ms measures responsiveness — critical for real-time applications.",
        f"Lower jitter ({jitter} ms) indicates more consistent connection quality.",
    ]
    return "\n".join(lines)


def format_iqi_summary(result: dict, country: str, metric: str) -> str:
    """Format Internet Quality Index summary into readable output."""
    summary = result.get("summary_0", {})
    meta = result.get("meta", {})

    date_range = meta.get("dateRange", [{}])
    start = date_range[0].get("startTime", "N/A") if date_range else "N/A"
    end = date_range[0].get("endTime", "N/A") if date_range else "N/A"

    metric_labels = {
        "bandwidth": "Bandwidth Quality Index",
        "latency": "Latency Quality Index",
        "dns": "DNS Response Quality Index",
    }

    lines = [
        f"Title: Internet Quality Index ({metric.title()}) in {country.upper()}",
        "",
        f"This measures the {metric_labels.get(metric, metric)} from the Cloudflare",
        "Radar Internet Quality Index (IQI). The IQI estimates end-user connection",
        "quality by analyzing real Cloudflare traffic patterns — not synthetic tests.",
        "",
        f"**Measurement Period:** {start} to {end}",
        "",
        f"**IQI {metric.title()} Summary:**",
        "",
        "| Percentile | Value |",
        "|------------|-------|",
    ]

    for key in sorted(summary.keys()):
        lines.append(f"| {key} | {summary[key]} |")

    lines.extend([
        "",
        "**Interpretation:**",
        "",
        f"The IQI {metric} values represent quality distribution across the country.",
        "Higher bandwidth values indicate better download capacity. Lower latency",
        "values indicate more responsive connections. These metrics are derived from",
        "actual Cloudflare traffic, providing a continuous quality measurement.",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch internet performance data from Cloudflare Radar API."
    )
    parser.add_argument("--country", required=True, help="ISO country code (e.g., AU, FR, SN)")
    parser.add_argument("--date-range", default="90d", help="Date range (default: 90d)")
    parser.add_argument("--metric", default=None,
                        help="IQI metric: bandwidth, latency, dns (default: fetch all)")
    args = parser.parse_args()

    try:
        client = RadarClient()
        country = args.country.upper()

        # ── Speed Summary ──
        print("=" * 60)
        print(f"📡  Fetching speed data for {country} (range: {args.date_range})...")
        print("=" * 60)

        try:
            speed_result = client.get_speed_summary(country, args.date_range)

            print("\n🔍 RAW API RESPONSE:")
            print(json.dumps(speed_result, indent=2)[:2000])

            print("\n✨ FORMATTED OUTPUT:")
            print(format_speed_summary(speed_result, country))
        except Exception as e:
            print(f"⚠️  Speed summary error: {e}")

        # ── IQI Metrics ──
        metrics = [args.metric] if args.metric else ["bandwidth", "latency", "dns"]

        for metric in metrics:
            print("\n" + "=" * 60)
            print(f"📊  Fetching IQI ({metric}) for {country}...")
            print("=" * 60)

            try:
                iqi_result = client.get_iqi_summary(country, metric, args.date_range)

                print("\n🔍 RAW API RESPONSE:")
                print(json.dumps(iqi_result, indent=2)[:2000])

                print("\n✨ FORMATTED OUTPUT:")
                print(format_iqi_summary(iqi_result, country, metric))
            except Exception as e:
                print(f"⚠️  IQI ({metric}) error: {e}")

        # ── Speed Histogram (Distribution Analysis) ──
        print("\n" + "=" * 60)
        print(f"📈  Fetching speed histogram for {country}...")
        print("=" * 60)

        try:
            histogram_result = client.get_speed_histogram(country, metric="downloadSpeed",
                                                          date_range=args.date_range)
            print("\n🔍 RAW API RESPONSE:")
            print(json.dumps(histogram_result, indent=2)[:2000])

            print("\n✨ INTERPRETATION:")
            print(f"Speed distribution for {country} — reveals inequality between")
            print("urban and rural areas. Narrow distribution = equitable access.")
        except Exception as e:
            print(f"⚠️  Speed histogram error: {e}")

        # ── TCP Resets & Timeouts (Connection Tampering) ──
        print("\n" + "=" * 60)
        print(f"🔒  Fetching TCP resets/timeouts for {country}...")
        print("=" * 60)

        try:
            tcp_result = client.get_tcp_resets_timeouts_summary(country, args.date_range)
            print("\n🔍 RAW API RESPONSE:")
            print(json.dumps(tcp_result, indent=2)[:2000])

            print("\n✨ INTERPRETATION:")
            print("High reset/timeout rates indicate connection tampering,")
            print("middlebox interference, or infrastructure instability.")
        except Exception as e:
            print(f"⚠️  TCP resets/timeouts error: {e}")

        # ── Traffic Anomalies (Outage Detection) ──
        print("\n" + "=" * 60)
        print(f"🚨  Fetching traffic anomalies for {country}...")
        print("=" * 60)

        try:
            anomaly_result = client.get_traffic_anomalies(country, args.date_range)
            print("\n🔍 RAW API RESPONSE:")
            print(json.dumps(anomaly_result, indent=2)[:2000])

            print("\n✨ INTERPRETATION:")
            print("Frequent anomalies indicate infrastructure fragility —")
            print("directly relevant to IRI resilience scoring.")
        except Exception as e:
            print(f"⚠️  Traffic anomalies error: {e}")

    except ValueError as e:
        print(f"\n❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
