### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures the responsiveness (latency and jitter) of mobile internet networks in a country. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides real-time latency and jitter measurements aggregated from speed tests run by real users. Mobile responsiveness is particularly critical because mobile networks inherently have higher latency and jitter than fixed-line networks due to wireless last-mile, handoffs between towers, and shared spectrum.

* **Data Source:** Cloudflare Radar API (`GET /radar/quality/speed/summary`)
* **Key Fields:**
    * `latencyIdle` — Median idle latency in milliseconds (round-trip time when the connection is not under load)
    * `jitterIdle` — Median idle jitter in milliseconds (variation in latency, indicating connection stability)
* **Supplementary Endpoints:**
    * `GET /radar/quality/iqi/summary` with `metric=latency` — Internet Quality Index for latency, normalized quality score
    * `GET /radar/quality/iqi/summary` with `metric=dns` — DNS resolution quality, critical for mobile browsing experience

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. In mobile-dominant markets, the aggregate latency naturally reflects mobile network characteristics. In mixed markets, it represents blended performance.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# Latency and jitter (combined fixed + mobile)
speed_data = client.get_speed_summary(country="KE", date_range="90d")
latency_ms = speed_data["summary_0"]["latencyIdle"]
jitter_ms = speed_data["summary_0"]["jitterIdle"]

# IQI latency quality index
iqi_latency = client.get_iqi_summary(country="KE", metric="latency")

# DNS resolution quality (impacts perceived mobile responsiveness)
iqi_dns = client.get_iqi_summary(country="KE", metric="dns")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country KE --metric latency
```

### Interpretation for IRI

* **Latency context for mobile:** Mobile networks typically have higher latency than fixed networks. A median of 30–60 ms is competitive for 4G/LTE. Below 20 ms suggests 5G deployment or strong CDN/IXP presence reducing distance to content. Above 100 ms indicates poor infrastructure — traffic likely routes through distant international hubs.
* **Jitter context for mobile:** Mobile jitter below 10 ms is acceptable for voice/video applications. Above 20 ms degrades real-time communication quality significantly. High jitter is often caused by congested cell towers, frequent handoffs, or overloaded backhaul links.
* **DNS quality:** Slow DNS resolution disproportionately affects mobile users who frequently open new connections (app launches, browsing). A low IQI DNS score suggests the country lacks local DNS resolvers or recursive infrastructure, forcing queries to route internationally.
* **Combined assessment:** A country with low latency but high jitter has inconsistent quality — the network performs well on average but is unreliable. For IRI scoring, consistency of responsiveness (low jitter) is as important as raw latency numbers.
