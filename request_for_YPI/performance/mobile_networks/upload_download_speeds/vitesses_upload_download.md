### IRI Indicator Analysis

This indicator, attached to the PERFORMANCE pillar, measures upload and download speed performance of mobile internet networks in a country. The original IRI data source is Ookla, but this project uses **Cloudflare Radar** as a direct, API-accessible replacement.

### Cloudflare Radar Integration — Active Indicator

* **Relevance Assessment:** Case A (Highly Relevant).

Cloudflare Radar provides real-time, continuously updated speed data aggregated from speed tests run by real users on speed.cloudflare.com. Mobile network performance is critical in countries where mobile connectivity dominates internet access — often the case in developing regions where fixed-line infrastructure is limited.

* **Data Source:** Cloudflare Radar API (`GET /radar/quality/speed/summary`)
* **Key Fields:**
    * `downloadSpeed` — Median download speed in Mbps
    * `uploadSpeed` — Median upload speed in Mbps
* **Supplementary Endpoints:**
    * `GET /radar/quality/speed/histogram` with `metric=downloadSpeed` or `metric=uploadSpeed` — full speed distribution analysis
    * `GET /radar/quality/speed/top/locations` — global ranking by speed metric for cross-country benchmarking

> **Note on Scope:** Cloudflare Radar does not differentiate between fixed and mobile networks. The data represents aggregate performance across all connection types. In countries where mobile traffic dominates (common in Africa, parts of Asia), the aggregate metric will naturally reflect mobile network characteristics. For countries with a balanced fixed/mobile split, the values represent blended performance.

### Integration Instructions

#### Method 1: Direct API Call (Python)

```python
from request_for_YPI.src.tools.cloudflare_radar import RadarClient

client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env

# Median download and upload speeds (combined fixed + mobile)
speed_data = client.get_speed_summary(country="SN", date_range="90d")
download_mbps = speed_data["summary_0"]["downloadSpeed"]
upload_mbps = speed_data["summary_0"]["uploadSpeed"]

# Speed distribution analysis
dl_histogram = client.get_speed_histogram(country="SN", metric="downloadSpeed")
ul_histogram = client.get_speed_histogram(country="SN", metric="uploadSpeed")

# Global ranking for benchmarking
top_download = client.get_speed_top_locations(metric="downloadSpeed")
```

#### Method 2: Test Runner

```bash
python testfiles/run_radar.py --country SN
```

### Interpretation for IRI

* **Download speed context:** In mobile-dominant markets, download speeds of 10–30 Mbps indicate solid 4G/LTE coverage. Speeds above 50 Mbps suggest emerging 5G infrastructure. Below 5 Mbps indicates reliance on 3G or congested shared spectrum.
* **Upload speed context:** Mobile upload speeds are typically lower than download (asymmetric by design). Median upload above 5 Mbps is adequate for basic content creation and cloud services. Below 2 Mbps limits productive mobile use.
* **Download/Upload ratio:** Mobile networks typically show ratios of 3:1 to 8:1. Extreme ratios (>10:1) indicate spectrum congestion on uplink channels.
* **Cross-country benchmarking:** Use `get_speed_top_locations()` to rank the target country against regional peers, providing context for whether the country's performance is competitive within its economic tier.
* **Histogram analysis:** In mobile-heavy markets, bimodal speed distributions often reveal the gap between 4G/5G-covered urban areas and 2G/3G-limited rural areas — a key input for IRI equity assessment.
