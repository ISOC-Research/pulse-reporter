### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures download speed performance of fixed internet networks in a country. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides real-time, continuously updated download speed data aggregated from speed tests run by real users on speed.cloudflare.com. Unlike Ookla's quarterly reports, Cloudflare Radar offers API-accessible data with configurable date ranges, making it ideal for automated IRI evaluation pipelines.

* **Data Source:** Cloudflare Radar API (`GET /radar/quality/speed/summary`)
* **Key Field:** `downloadSpeed` (median download speed in Mbps)
* **Supplementary Endpoint:** `GET /radar/quality/speed/histogram` with `metric=downloadSpeed` — provides the full speed distribution across the country, revealing inequality between urban and rural areas.

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. The download speed value should be interpreted as a blended national metric.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# Median download speed
speed_data = client.get_speed_summary(country="FR", date_range="90d")
download_mbps = speed_data["summary_0"]["downloadSpeed"]

# Distribution analysis (inequality check)
histogram = client.get_speed_histogram(country="FR", metric="downloadSpeed")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country FR
```

### Interpretation for IRI

* **High download speeds (>50 Mbps median):** Indicates strong fixed-line infrastructure, likely supported by fiber or cable deployments.
* **Low download speeds (<10 Mbps median):** Signals infrastructure underinvestment or dominance of legacy technologies (DSL, satellite).
* **Histogram analysis:** A narrow distribution (most users clustered around the median) indicates equitable access. A wide, bimodal distribution signals a digital divide between well-served and underserved populations.
