# Automated Recommendation Engine for Enhancing Internet Resilience

## Overview

An agentic system that combines technical infrastructure data from the Internet Yellow Pages (IYP) Neo4j database with real-time web research to generate comprehensive policy recommendations for improving national internet resilience. The engine uses a two-phase AI approach: investigative research followed by strategic synthesis.

## Purpose

The Internet Resilience Index (IRI) measures a country's internet resilience across four pillars, but understanding why scores are low and what to do requires both technical analysis and contextual understanding. This project automates that process by:

1. Querying infrastructure and network topology data from Neo4j
2. Conducting web research for policy context, recent events, and regulations
3. Synthesizing both data streams into actionable strategic reports
4. Providing prioritized recommendations with implementation roadmaps

## Architecture
```
pulse-reporter/
├── dnssec_report.py              # DNSSEC analysis report generator
├── ipv6_report.py                # IPv6 deployment analysis
├── generate_llm_brief.py         # LLM-based brief generation
├── data/
│   └── tld_trend_history.json   # Historical TLD trend data
├── reports/                      # Generated analysis reports
│   ├── DNSSEC_*.md
│   └── IPv6_*.md
├── request_for_YPI/              # Main agentic engine
│   ├── generate_report.py        # Main orchestrator (two-phase workflow)
│   ├── gene_report_v2.py         # Report generation v2
│   ├── pulse_service.py          # Pulse data service
│   ├── dnssec_engine.py          # DNSSEC-specific engine
│   ├── dnssec_radar_engine.py    # DNSSEC radar integration
│   ├── ipv6_engine.py            # IPv6-specific engine
│   ├── apnic_service.py          # APNIC data service
│   ├── crux_service.py           # Chrome UX Report service
│   ├── src/
│   │   ├── agents/               # LangGraph agent definitions
│   │   ├── tools/                # Tool implementations (Neo4j, Google Search, etc.)
│   │   ├── RAG/                  # RAG pipeline components
│   │   └── utils/                # Utilities (LLM config, formatters, loaders)
│   ├── prompt/                   # LLM prompt templates
│   │   ├── IYP/                  # IYP-specific prompts
│   │   ├── report_generation/    # Report generation prompts
│   │   └── *.txt                 # Prompt strategies
│   ├── infrastructure/           # Pillar 1: IXPs, data centers, fiber
│   ├── market_readiness/         # Pillar 2: Market structure, peering
│   ├── performance/              # Pillar 3: Speed & consistency metrics
│   ├── security/                 # Pillar 4: DNS, routing, threat analysis
│   └── schema_rapport/           # Report schema definitions
├── schema_rapport/
│   └── schema_global.py          # Global report schema
├── testfiles/                    # Testing utilities
│   ├── request_testing.py        # Query testing framework
│   ├── run_query.py              # Query execution tool
│   ├── run_radar.py              # Radar query testing
│   └── unit_test_request.py      # Validation suite
├── web/
│   └── back.py                   # Web backend API
└── requirements.txt              # Project dependencies
```

Each indicator directory (under infrastructure/, market_readiness/, performance/, security/) contains:
- `*.cypher` - Progressive Cypher queries building complete analysis
- `*.md` - Technical documentation and analysis plans
- `query_templates.yaml` - Jinja2 templates for formatting Neo4j results

## Report Generators

- **dnssec_report.py** - Generates DNSSEC deployment and security analysis reports
- **ipv6_report.py** - Analyzes IPv6 infrastructure adoption and readiness
- **generate_llm_brief.py** - Creates AI-powered executive briefs from analysis data

## Two-Phase Agentic Architecture

### Phase 1: Investigation (Agentic Research)

Uses LangGraph to orchestrate an autonomous agent that:
- Executes Neo4j queries via the `run_infrastructure_query` tool
- Searches the web for policy documents, news, and regulations via `search_google`
- Reads and extracts content from web pages and PDFs via `read_web_page`
- Decides autonomously which tools to use and when to stop researching

Model: Google Gemini Flash (2.0)

### Phase 2: Strategic Synthesis (Reasoning Mode)

Uses a reasoning model to:
- Analyze the complete investigation history
- Correlate quantitative metrics with qualitative context
- Perform root cause analysis linking technical issues to policy gaps
- Generate comprehensive reports following expert prompt structure
- Provide prioritized, actionable recommendations

Model: Google Gemini Pro 2.0 (with extended thinking)

## IRI Coverage

Fully Supported Indicators:
- IXP Coverage, Peering Efficiency, Domain Analysis
- Market Competition (HHI), Transit Dependency
- MANRS Adoption, IPv6 Deployment, DNSSEC Analysis
- DDoS Protection (CDN presence)

Not Supported:
- Performance metrics (requires Ookla data)
- HTTPS adoption (requires certificate data)
- Economic indicators (requires external pricing data)

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Database Setup

 - Use Internet Society's Public Instance:
```python
URI = 'neo4j://iyp-bolt.ihr.live:7687'
AUTH = None
```


### API Keys Configuration

Create a `.env` file:
```bash
GOOGLE_API_KEY=your_key
GOOGLE_CX_ID=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_PROJECT=your_key
LANGCHAIN_ENDPOINT=your_key
LANGCHAIN_TRACING_V2="True"
```
### Obtaining API Keys

**Google Gemini API**: Visit https://console.cloud.google.com to create a project, enable the Gemini API, and generate an API key from the Credentials page.

**Google Custom Search**: Visit https://console.cloud.google.com to create a project, enable the Custom Search API, and generate credentials. Then create a Custom Search Engine at https://programmablesearchengine.google.com to obtain your CX ID.

**LangSmith** (Optional): Sign up at https://smith.langchain.com for conversation tracing and debugging. Free tier available for development.


### Usage

#### Generate Full Analysis Reports

DNSSEC analysis:
```bash
python dnssec_report.py --country=FR
```

IPv6 analysis:
```bash
python ipv6_report.py --country=IN
```

Generate comprehensive IRI indicator report:
```bash
python request_for_YPI/generate_report.py infrastructure/ixp_coverage --country=FR --mode=smart
```

Report parameters:
- `indicator_input`: Partial or full path to indicator folder
- `--country`: ISO country code (default: FR)
- `--domain`: Domain name for analysis (default: gouv.fr)
- `--asn`: AS number (default: 16276)
- `--mode`: Research phase model - 'fast' or 'smart' (default: smart)

Generate AI brief:
```bash
python generate_llm_brief.py --report=reports/DNSSEC_FR_20260620_1623.md
```

### Testing & Validation

Test a single Neo4j query:
```bash
python testfiles/request_testing.py request_for_YPI/security/dns_security/dnssec/1.cypher --country=FR
```

Test query with LLM formatting preview:
```bash
python testfiles/run_query.py request_for_YPI/performance/fixed_networks/vitesses_download/1.cypher --country=FR
```

Test radar data queries:
```bash
python testfiles/run_radar.py --country=IN
```

Run full validation suite:
```bash
python testfiles/unit_test_request.py
```

## Report Structure

Generated reports include:

1. Executive Summary - Current state, key findings, resilience assessment
2. Detailed Technical Analysis - Quantitative metrics with qualitative context
3. Risk Assessment Matrix - Technical, operational, and strategic risks
4. Strategic Recommendations Framework
   - Short-term (0-12 months)
   - Medium-term (1-3 years)
   - Long-term (3-5 years)
   - Each with: complexity, cost, impact, stakeholders, KPIs
5. Prioritization Framework - Quick wins vs strategic investments
6. Implementation Roadmap - Quarterly breakdown with dependencies
7. Measurement & Monitoring Framework - KPIs and review schedule
8. Risk Mitigation & Contingency Planning
9. Funding Strategy
10. International Best Practices & Case Studies

## Key Concepts

- **IRI**: Internet Resilience Index - Composite score measuring resilience across Infrastructure, Market Preparation, Performance, and Security pillars
- **IYP**: Internet Yellow Pages - Graph database mapping global internet topology, peering relationships, and routing security
- **Agentic Workflow**: AI agent autonomously decides which data sources to query and when sufficient information has been gathered
- **Two-Phase Architecture**: Separate research phase (breadth) from synthesis phase (depth)
- **Query Pattern**: Overview → Metrics → Gaps → Recommendations

## LLM Modes

The system supports two operational modes:

- **fast**: Google Gemini Flash 2.0 - Quick processing for web scraping and summarization
- **reasoning**: Google Gemini Pro 2.0 - Advanced reasoning for strategic synthesis (Phase 2 only)

## Development

Adding new indicators:

1. Create directory under appropriate pillar
2. Write progressive `.cypher` queries (1.cypher, 2.cypher, etc.)
3. Document analysis approach in `.md` file
4. Add formatting templates in `query_templates.yaml`
5. Test with validation suite: `python testfiles/unit_test_request.py`

## Output

Reports are generated in multiple formats:

1. **Analysis Reports** - Saved in `reports/` directory:
   - DNSSEC analysis: `DNSSEC_{CC}_{timestamp}.md`
   - IPv6 analysis: `IPv6_{CC}_{timestamp}.md`

2. **IRI Indicator Reports** - Saved in indicator directories:
   - Format: `report_{indicator_name}_countryCode-{CC}_domainName-{domain}_hostingASN-{asn}.md`

3. **Web Interface** - Viewable via web backend:
   - HTML report preview: `web/result.html`
   - Markdown rendering: `web/result_markdown.html`

## Dependencies

Core libraries:
- neo4j - Database connectivity
- langchain / langgraph - Agentic framework
- langchain-google-genai - LLM integration
- trafilatura - Web content extraction
- PyMuPDF - PDF text extraction
- Jinja2 / PyYAML - Template rendering
- requests / beautifulsoup4 - HTTP and parsing

## Key Features

- **Multi-pillar Analysis**: Covers Infrastructure, Market Readiness, Performance, and Security
- **Neo4j Integration**: Direct connectivity to Internet Yellow Pages database
- **Web Research**: Autonomous agent conducts Google searches for policy context
- **PDF Processing**: Extracts and analyzes policy documents and technical papers
- **LLM-powered Synthesis**: Reasoning models generate strategic recommendations
- **DNSSEC & IPv6 Focus**: Specialized engines for DNS security and IPv6 deployment analysis
- **Radar Integration**: Cloudflare Radar for DNS and threat analysis data
- **Web Interface**: Visual browsing of generated reports

## Status

Active Development | Version 0.4 | Last Updated: June 2026