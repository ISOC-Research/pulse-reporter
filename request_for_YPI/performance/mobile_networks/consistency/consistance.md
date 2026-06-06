### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures the consistency of mobile internet network performance in a country — how uniformly mobile users experience internet quality across regions, times of day, and network conditions. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides two complementary data sources for mobile consistency measurement:

1. **Internet Quality Index (IQI) — Bandwidth:** The IQI bandwidth metric reports percentile distributions (p25, p50, p75) of connection quality. The inter-quartile range (IQR) directly measures consistency: a narrow IQR means most users get similar quality; a wide IQR signals inequality.
2. **Speed Histogram:** The speed distribution histogram reveals whether the mobile population clusters around a single performance tier or is split across multiple tiers. In mobile-dominant markets, this effectively captures the consistency of the mobile experience.

* **Primary Data Source:** Cloudflare Radar API (`GET /radar/quality/iqi/summary`) with `metric=bandwidth`
* **Key Fields:** Percentile values (p25, p50, p75) — the IQR (p75 − p25) is the primary consistency metric.
* **Supplementary Endpoints:**
    * `GET /radar/quality/speed/histogram` with `metric=downloadSpeed` — granular distribution analysis
    * `GET /radar/quality/iqi/timeseries_groups` with `metric=bandwidth` — time-series consistency to detect performance degradation patterns (peak-hour congestion)

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. In countries where mobile traffic dominates internet access (common in developing regions), the IQI and histogram data will naturally reflect mobile consistency characteristics.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# IQI bandwidth percentile distribution (consistency proxy)
iqi_data = client.get_iqi_summary(country="NG", metric="bandwidth")
# Extract percentiles from iqi_data["summary_0"]

# Speed distribution histogram (granular consistency view)
histogram = client.get_speed_histogram(country="NG", metric="downloadSpeed")

# Time-series consistency (detect peak-hour degradation)
timeseries = client.get_iqi_timeseries(country="NG", metric="bandwidth")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country NG --metric bandwidth
```

### Interpretation for IRI

* **Narrow IQR (p75/p25 ratio < 2):** Highly consistent mobile experience — most users receive similar quality regardless of location or time. This is rare in mobile-dominant markets but indicates strong infrastructure investment.
* **Wide IQR (p75/p25 ratio > 5):** Significant performance inequality — likely reflecting the gap between 4G/5G-covered urban areas and 2G/3G-limited rural zones. This is the most common pattern in developing countries with rapid but uneven mobile rollout.
* **Histogram shape for mobile markets:**
    * **Unimodal, narrow peak:** Strong consistency — one dominant mobile technology tier (e.g., widespread 4G).
    * **Bimodal distribution:** Classic urban/rural digital divide — 4G in cities, 2G/3G elsewhere. This pattern is the strongest negative signal for IRI consistency.
    * **Long tail toward low speeds:** Underserved minority, often geographically remote or on legacy networks.
* **Time-series patterns:** Consistent IQI scores across hours of the day indicate well-provisioned infrastructure. Significant dips during business hours or evenings indicate capacity constraints — cell towers congested by peak usage.
* **Mobile-specific insight:** Mobile consistency is often more variable than fixed consistency because mobile users share spectrum, experience signal quality variations, and are subject to cell tower congestion. A country with high mobile consistency has invested in dense cell tower deployment and sufficient backhaul capacity.
