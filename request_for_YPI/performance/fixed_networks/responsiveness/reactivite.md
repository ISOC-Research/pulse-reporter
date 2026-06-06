### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures the responsiveness (latency and jitter) of fixed internet networks in a country. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides real-time latency and jitter measurements aggregated from speed tests run by real users on speed.cloudflare.com. Responsiveness is critical for real-time applications (VoIP, video conferencing, online gaming, financial transactions) and is a key IRI performance dimension.

* **Data Source:** Cloudflare Radar API (`GET /radar/quality/speed/summary`)
* **Key Fields:**
    * `latencyIdle` — Median idle latency in milliseconds (round-trip time when the connection is not under load)
    * `jitterIdle` — Median idle jitter in milliseconds (variation in latency, indicating connection stability)
* **Supplementary Endpoint:** `GET /radar/quality/iqi/summary` with `metric=latency` — provides the Internet Quality Index for latency, a normalized quality score derived from real Cloudflare traffic patterns.

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. Latency and jitter values should be interpreted as blended national metrics.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# Latency and jitter
speed_data = client.get_speed_summary(country="FR", date_range="90d")
latency_ms = speed_data["summary_0"]["latencyIdle"]
jitter_ms = speed_data["summary_0"]["jitterIdle"]

# IQI latency quality index (normalized score)
iqi_data = client.get_iqi_summary(country="FR", metric="latency")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country FR --metric latency
```

### Interpretation for IRI

* **Low latency (<20 ms median):** Excellent responsiveness, typical of countries with dense local infrastructure (IXPs, CDN PoPs, short last-mile distances).
* **High latency (>100 ms median):** Indicates poor infrastructure — traffic may be routing through distant international hubs rather than staying local. This is common in countries with few IXPs or where major content is hosted abroad.
* **Low jitter (<5 ms):** Stable, consistent connections suitable for real-time applications.
* **High jitter (>20 ms):** Unstable connections, often due to congested links, wireless last-mile, or poorly maintained infrastructure. High jitter degrades voice/video quality even when average latency is acceptable.
* **IQI latency score:** A normalized quality metric (0–1 scale) that contextualizes raw latency against global benchmarks — useful for cross-country IRI comparisons.
