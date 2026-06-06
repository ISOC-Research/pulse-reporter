### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures upload speed performance of fixed internet networks in a country. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides real-time, continuously updated upload speed data aggregated from speed tests run by real users on speed.cloudflare.com. Unlike Ookla's quarterly reports, Cloudflare Radar offers API-accessible data with configurable date ranges, making it ideal for automated IRI evaluation pipelines.

* **Data Source:** Cloudflare Radar API (`GET /radar/quality/speed/summary`)
* **Key Field:** `uploadSpeed` (median upload speed in Mbps)
* **Supplementary Endpoint:** `GET /radar/quality/speed/histogram` with `metric=uploadSpeed` — provides the full speed distribution across the country, revealing asymmetry between download and upload capacity.

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. The upload speed value should be interpreted as a blended national metric.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# Median upload speed
speed_data = client.get_speed_summary(country="FR", date_range="90d")
upload_mbps = speed_data["summary_0"]["uploadSpeed"]

# Distribution analysis
histogram = client.get_speed_histogram(country="FR", metric="uploadSpeed")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country FR
```

### Interpretation for IRI

* **High upload speeds (>20 Mbps median):** Indicates symmetric or near-symmetric infrastructure (fiber), enabling content creation, cloud services, and remote work.
* **Low upload speeds (<5 Mbps median):** Signals asymmetric infrastructure (ADSL, cable) where users are consumers rather than producers of content. This limits the country's ability to host local services and content.
* **Download/Upload ratio:** A ratio above 10:1 indicates heavily asymmetric infrastructure. Countries with ratios below 3:1 have more resilient, fiber-based networks that support bidirectional traffic.
* **Histogram analysis:** A narrow distribution indicates consistent upload quality. A wide distribution signals infrastructure inequality.
