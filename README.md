# ISOC Pulse Diagnostics Report & Action Plan Generator

An automated Internet measurement analytics engine that transforms deterministic network telemetry from **ISOC Pulse**, **Internet Yellow Pages (IYP)**, **PeeringDB**, **Packet Clearing House (PCH)**, **RIPEstat / RIPE Atlas**, and **Cloudflare Radar** into institutional-grade country diagnostics reports and action plans.

The engine generates both interactive web dashboards (`.html`) and official publication-ready Word documents (`.docx`) strictly styled after the master ISOC Pulse Country Report template.

---

## Supported Pillars & Metrics

1. **Interconnection & Peering** (`peering`):
   - Macro ASN landscape (registered vs. actively routed in BGP)
   - IXP infrastructure, operational status, and member networks
   - IXP geographic distribution and market concentration (HHI)
   - Aggregated IXP traffic telemetry from PCH
   - Domestic ASN peering participation & route server adoption
   - Global Tier-1 CDN presence at domestic IXPs vs. local data center facilities
   - Domestic traffic localization ratio (ISOC Pulse IRI)
   - RIPE Atlas traceroute path analysis for domestic tromboning (boomerang routing) and edge content latency

2. **IPv6 Deployment** (`ipv6`):
   - National user adoption trends and regional/global benchmarks
   - ISP market share vs. per-operator IPv6 deployment & RPKI/ROV coverage
   - Public and private web services IPv6 readiness (Government, Banking, News, Education, Ecommerce)
   - CDN-backed vs. self-hosted IPv6 correlation
   - ccTLD nameserver IPv6 reachability and glue record health

3. **DNSSEC Deployment** (`dnssec`):
   - ccTLD authoritative nameserver count, IPv6 enablement, and ASN diversity
   - National DNS query resolution health (NOERROR, NXDOMAIN, SERVFAIL)
   - Resolver DNSSEC validation rates (Secure vs. Insecure)
   - Per-operator / per-ASN validation performance across major eyeball networks

---

## Project Structure

```
pulse-reporter/
├── run.py                       # Unified CLI launcher for all metrics and pipelines
├── peering_report.py            # Peering engine: PeeringDB, PCH, RIPEstat, Atlas, Pulse
├── ipv6_report.py               # IPv6 engine: IYP Neo4j, Pulse, APNIC Labs, CrUX
├── dnssec_report.py             # DNSSEC engine: IYP Neo4j, Cloudflare Radar
├── generate_llm_brief.py        # Strategic synthesis engine: HTML dashboard & Word builder
│
├── isoc_report.py               # 10-section ISOC report prompt, quota fallback, HTML cleaner
├── isoc_theme.py                # Official ISOC color palette (#0F2A47 navy) and font constants
├── docx_builder.py              # Word document builder with automated TOC page refresh
├── docx_charts.py               # 200 DPI matplotlib chart generator (donut, bar, line, matrix)
├── html_theme.py                # Interactive web dashboard styling & inline chart renderer
├── build_template.py            # Clones ISOC_Sample.docx into master Word template
│
├── templates/
│   └── ISOC_Template.docx       # Official Word report template
├── data/
│   └── tld_trend_history.json   # Historical TLD trend data
├── reports/                     # Organized report repository
│   ├── peering/                 # {raw/*.md, html/*.html, word/*.docx}
│   ├── ipv6/                    # {raw/*.md, html/*.html, word/*.docx}
│   └── dnssec/                  # {raw/*.md, html/*.html, word/*.docx}
└── request_for_YPI/             # API services and Cypher indicator library
    ├── peering_engine.py        # Core peering aggregation pipeline
    ├── ipv6_engine.py           # Core IPv6 data aggregation pipeline
    ├── dnssec_engine.py         # DNSSEC nameserver & IPv6 engine
    ├── dnssec_radar_engine.py   # Cloudflare Radar query service
    ├── pulse_service.py         # ISOC Pulse REST API integration
    ├── apnic_service.py         # APNIC Labs IPv6 adoption integration
    ├── crux_service.py          # Google Chrome UX Report integration
    └── src/
        ├── request_IYP/         # Neo4j Cypher query execution
        └── tools/               # Cloudflare Radar client
```

---

## Quick Start

### 1. Setup Environment
```bash
conda activate pulse_env
# Or with venv:
# pip install -r requirements.txt
```

### 2. Configure Credentials (`.env`)
Create a `.env` file in `pulse-reporter/` with:
```env
REPORT_GEN_KEY=your_gemini_api_key
INTERNET_SOCIETY_API_KEY=your_isoc_pulse_key
CLOUDFLARE_RADAR_API_TOKEN=your_radar_token
PEERINGDB_API_KEY=your_peeringdb_key
RIPE_ATLAS_API_KEY=your_ripe_atlas_key
GOOGLE_APPLICATION_CREDENTIALS=your_crux_key.json
NEO4J_URI=neo4j://iyp-bolt.ihr.live:7687
```

---

## Running Reports

Use the unified launcher `run.py`. Argument order and capitalization do not matter (`python run.py peering IN` and `python run.py IN peering` both work).

### Full Pipeline (Fetches live data + Generates HTML & Word docx)
```bash
python run.py peering IN          # Full Peering report for India
python run.py ipv6 IN             # Full IPv6 report for India
python run.py dnssec IN           # Full DNSSEC report for India
python run.py all IN              # Run ALL 3 metrics for India
```
*(Replace `IN` with any 2-letter ISO country code: `FR`, `BR`, `MA`, `SO`, `US`, `DE`, etc.)*

### Step-by-Step Modes (Optional Flags)
* **Step 1 Only (`--raw`):** Fetch/update the raw `.md` data file without invoking the LLM:
  ```bash
  python run.py peering IN --raw
  ```
* **Step 2 Only (`--brief`):** Generate/rebuild `.html` and `.docx` reports from an existing `.md` file (skips live API queries):
  ```bash
  python run.py peering IN --brief
  python run.py ipv6 IN --brief
  python run.py dnssec IN --brief
  ```

### Student Wi-Fi / Restricted Networks Note
When on restricted campus or corporate Wi-Fi where Neo4j Bolt port `7687` is blocked:
* **Peering (`run.py peering <CC>`):** Works 100% live for ANY country because it uses HTTPS REST APIs (PeeringDB, PCH, RIPEstat, Pulse, RIPE Atlas).
* **IPv6 & DNSSEC:** Running `run.py <metric> <CC>` automatically falls back to pre-fetched raw `.md` data (e.g., `IN`, `FR`, `MA`, `SO`) to generate the HTML and Word documents.

---

## Report Structure (10-Section Master Template)

Every generated report adheres to the official ISOC Pulse 10-section hierarchy:

1. **Executive summary** (2–3 dense analytical paragraphs summarizing standing and paradox)
2. **Key numbers at a glance** (4-column table: Indicator | Country | Benchmark | Reading)
3. **1. Where [Country] stands** (Benchmark comparison analysis + inline bar chart)
4. **2. Where [Country] is improving** (Numbered subsections 2.1–2.4 with inline tables/charts)
5. **3. Where [Country] could improve** (Bottlenecks: concentration, peering gaps, security)
6. **4. A staged plan to improve resilience** (Effort vs. Impact matrix + Short/Medium/Long-term action tables)
7. **5. Quick wins** (Configuration/policy flags requiring zero capital)
8. **6. Policy gaps and loopholes** (Unenforced gaps + loopholes to avoid creating)
9. **7. Measuring progress** (Verifiable 12-month indicator targets and public sources)
10. **Conclusion & Data sources** (Methodology notes, caveats, and citations)

---

## Quality Control & Visual Consistency Rules

All reports are processed through an automated quality-control pipeline (`isoc_report.py`, `docx_charts.py`, `docx_builder.py`) enforcing:

1. **Strict 5-Action Quick Wins Alignment**:
   - Section 4.1 (Short term: 0–12 months) and Section 5 (Quick wins) contain the exact same 5 actions numbered `1` to `5`.
   - The *Prioritisation: impact versus effort* scatter plot strictly maps items `1`–`5` inside the green `QUICK WINS` zone (`effort < 4.5`), and items `6`–`10` inside the `STRUCTURAL INVESTMENT` zone (`effort > 4.5`).
2. **Concrete Operational Timeframes**:
   - Replaces generic `"Low"` / `"Medium"` labels with concrete engineering timeframes (e.g., `"2–4 weeks of IXP outreach"`, `"Days of operator work"`, `"Hours per network"`).
   - Expects baseline-to-target shifts in the `Expected effect` column.
3. **Zero Duplicate Tables**:
   - Eliminates redundant 2-column summary tables across Sections 2 and 3, replacing them with granular multi-column breakdowns (City-by-City IXP distribution, PCH telemetry reporting, and Tier-1 CDN presence matrices).
4. **Populated Reference Benchmarks**:
   - `Benchmark` column in "Key numbers at a glance" populates target thresholds (`>50% target`, `100% target`, `9 of 9 global`, `0% ideal`, `<20 ms target`) rather than empty em-dashes.
5. **Matplotlib Chart UI Refinements**:
   - **Donut Charts**: Enforces a 2-line center callout layout (bold metric on top, descriptive unit below) to prevent text overflow.
   - **Bar Charts**: Benchmark legends anchored to the top-right outside the plotting canvas (`bbox_to_anchor=(1.0, 1.02)`) with 15% upper x-axis padding (`max_val * 1.15`) to eliminate bar and label collision.
   - **Target Lines**: Eliminates duplicate parenthetical labels (e.g., `Target (>50%)` instead of `Target (>50%) (50%)`).
6. **Country-Specific Deep Links**:
   - Generates direct, verifiable links in "Data sources and notes" pointing directly to country reports on ISOC Pulse, RIPEstat, and PeeringDB.

---

## Output Organization

Outputs are organized under `reports/` by metric and format for all supported countries (**India `IN`**, **France `FR`**, **Somalia `SO`**, and **Morocco `MA`**):

| Metric | Word Document (`.docx`) | Interactive Dashboard (`.html`) | Raw Data (`.md`) |
| :--- | :--- | :--- | :--- |
| **Peering** | `reports/peering/word/Peering_Report_<CC>.docx` | `reports/peering/html/Peering_Policy_Brief_<CC>.html` | `reports/peering/raw/Peering_Report_<CC>.md` |
| **IPv6** | `reports/ipv6/word/IPv6_Report_<CC>.docx` | `reports/ipv6/html/IPv6_Policy_Brief_<CC>.html` | `reports/ipv6/raw/IPv6_Report_<CC>.md` |
| **DNSSEC** | `reports/dnssec/word/DNSSEC_Report_<CC>.docx` | `reports/dnssec/html/DNSSEC_Policy_Brief_<CC>.html` | `reports/dnssec/raw/DNSSEC_Report_<CC>.md` |

Each HTML dashboard includes a fixed **"Download Word report (.docx)"** button linking directly to the corresponding Word document.
