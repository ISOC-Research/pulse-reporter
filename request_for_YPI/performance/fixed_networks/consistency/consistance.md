### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures the consistency of fixed internet network performance in a country — how uniformly users experience internet quality. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides two complementary data sources for consistency measurement:

1. **Internet Quality Index (IQI) — Bandwidth:** The IQI bandwidth metric reports percentile distributions (p25, p50, p75) of connection quality across the country. A narrow spread between percentiles indicates consistent performance; a wide spread indicates inequality.
2. **Speed Histogram:** The speed distribution histogram reveals whether the population clusters around a single performance tier or is split across multiple tiers (bimodal distribution = digital divide).

* **Primary Data Source:** Cloudflare Radar API (`GET /radar/quality/iqi/summary`) with `metric=bandwidth`
* **Key Fields:** Percentile values (p25, p50, p75) — the inter-quartile range (IQR) is the primary consistency metric.
* **Supplementary Endpoint:** `GET /radar/quality/speed/histogram` with `metric=downloadSpeed` — provides full distribution buckets for granular analysis.

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. Consistency metrics should be interpreted as blended national metrics.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# IQI bandwidth percentile distribution (consistency proxy)
iqi_data = client.get_iqi_summary(country="FR", metric="bandwidth")
# Extract percentiles from iqi_data["summary_0"]

# Speed distribution histogram (granular consistency view)
histogram = client.get_speed_histogram(country="FR", metric="downloadSpeed")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country FR --metric bandwidth
```

### Interpretation for IRI

* **Narrow IQR (p75/p25 ratio < 2):** Highly consistent network — most users experience similar quality. Typical of countries with uniform fiber rollout or strong regulatory quality-of-service requirements.
* **Wide IQR (p75/p25 ratio > 5):** Significant performance inequality — likely a divide between urban (high-speed) and rural (low-speed) users, or between different ISPs with vastly different infrastructure investment levels.
* **Histogram shape:**
    * **Unimodal, narrow peak:** Excellent consistency — one dominant technology tier serving most of the population.
    * **Bimodal distribution:** Digital divide — two distinct population groups with different service levels (e.g., fiber vs. DSL, urban vs. rural).
    * **Long tail toward low speeds:** A minority of the population is underserved, which drags down the country's IRI consistency score.
* **Consistency is a multiplier:** A country with moderate median speeds but high consistency may score better on IRI than a country with high median speeds but extreme inequality, because consistency reflects equitable access — a core resilience dimension.
