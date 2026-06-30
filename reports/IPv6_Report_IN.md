# IPv6 Policy Brief — IN
**Generated:** 2026-06-26 08:20  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

IN currently has a national IPv6 adoption rate of 78.4%, with 0.2% of the subscriber market served by ISPs classified as non-compliant. 1 ISP(s) (covering 0.2% of the market) have zero IPv6 prefixes in the global routing table and require immediate regulatory intervention for RIR membership.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 25,831  
**RPKI-Covered Prefixes:** 7,403  
**RPKI Coverage:** 28.66%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| VIL-AS-AP Vodafone Idea Ltd | 1135 | 0.00% |
| TATAPLAYBROADBAND-AS-AP TATA PLAY BROADB | 635 | 0.00% |
| DNA-AS-AP DIGITAL NETWORK ASSOCIATES PRI | 102 | 0.00% |
| GTPL-AS-AP Gujarat Telelink Pvt Ltd | 285 | 0.35% |
| INPL-IN-AP Ishans Network | 156 | 0.64% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 227  
**IPv6-Capable Upstream Reachability:** 99.56%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 40  
**IXPs with IPv6 LAN:** 34 (85.0%)  
**Members with IPv6 Peering:** 1465 / 1895 (77.3%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| DE-CIX Mumbai | Yes | 453 | 318 | 70.2% |
| Extreme IX Mumbai | Yes | 249 | 201 | 80.7% |
| NIXI Mumbai | Yes | 177 | 146 | 82.5% |
| Extreme IX Delhi | Yes | 175 | 137 | 78.3% |
| NIXI Delhi | Yes | 117 | 89 | 76.1% |
| Extreme IX Chennai | Yes | 91 | 73 | 80.2% |
| DE-CIX Delhi | Yes | 88 | 66 | 75.0% |
| AMS-IX Mumbai | Yes | 80 | 57 | 71.2% |
| DE-CIX Chennai | Yes | 73 | 53 | 72.6% |
| NIXI Chennai | Yes | 59 | 52 | 88.1% |
| Extreme IX Bangalore | Yes | 39 | 35 | 89.7% |
| Kolkata IX | Yes | 31 | 29 | 93.5% |
| NIXI Kolkata | Yes | 30 | 27 | 90.0% |
| ANI-IX Delhi | Yes | 30 | 15 | 50.0% |
| Extreme IX Kolkata | Yes | 24 | 22 | 91.7% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 78.4%  
**Underserved Market Share:** 0.2%  
**ISPs Assessed:** 25

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS55836 | RELIANCEJIO-IN Reliance Jio Infocom | 46.3% | 5052 | 18 | 77.3% | **OK** — Compliant | Low | +10.5 pp |
| AS45609 | BHARTI-MOBILITY-AS-AP Bharti Airtel | 22.0% | 7177 | 1 | 69.7% | **OK** — Compliant | Low | +6.7 pp |
| AS24560 | AIRTELBROADBAND-AS-AP Bharti Airtel | 8.3% | 1026 | 1 | 65.4% | **OK** — Compliant | Low | +2.9 pp |
| AS9829 | BSNL-NIB National Internet Backbone | 3.0% | 2137 | 67 | 63.7% | **OK** — Compliant | Medium | +1.1 pp |
| AS38266 | VIL-AS-AP Vodafone Idea Ltd | 1.4% | 2683 | 1 | 63.2% | **OK** — Compliant | Low | +0.5 pp |
| AS133982 | EXCITEL-AS-IN Excitel Broadband Pri | 0.9% | 98 | 5 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS24309 | CABLELITE-AS-AP Atria Convergence T | 0.9% | 220 | 8 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS138754 | KVBPL-AS-IN Kerala Vision Broad Ban | 0.8% | 38 | 2 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS133661 | NETPLUS-AS Netplus Broadband Servic | 0.8% | 58 | 6 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS45916 | GTPL-AS-AP Gujarat Telelink Pvt Ltd | 0.7% | 570 | 10 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS45271 | VIL-AS-AP Vodafone Idea Ltd | 0.7% | 2271 | 1 | 63.0% | **OK** — Compliant | Low | +0.3 pp |
| AS17488 | HATHWAY-NET-AP Hathway IP Over Cabl | 0.6% | 100 | 4 | 62.9% | **OK** — Compliant | Low | +0.2 pp |
| AS24186 | RAILTEL-AS-IN RailTel Corporation o | 0.5% | 273 | 27 | 62.9% | **OK** — Compliant | Low | +0.2 pp |
| AS23860 | ALLIANCE-GATEWAY-AS-AP Alliance Bro | 0.5% | 605 | 6 | 62.9% | **OK** — Compliant | Low | +0.2 pp |
| AS17665 | ONEBROADBAND ONEOTT INTERTAINMENT L | 0.5% | 207 | 71 | 62.9% | **OK** — Compliant | Medium | +0.2 pp |
| AS55577 | CABLELITE-AS-AP Atria Convergence T | 0.4% | 118 | 1 | 62.9% | **OK** — Compliant | Low | +0.2 pp |
| AS134674 | TATAPLAYBROADBAND-AS-AP TATA PLAY B | 0.3% | 1239 | 7 | 62.9% | **OK** — Compliant | Low | +0.1 pp |
| AS18209 | CABLELITE-AS-AP Atria Convergence T | 0.3% | 66 | 5 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS17465 | ASIANET Cable ISP in India | 0.3% | 54 | 5 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS132116 | ANINETWORK-IN Ani Network Pvt Ltd | 0.2% | 56 | 80 | 62.8% | **OK** — Compliant | Medium | +0.1 pp |
| AS17917 | QTLTELECOM-AS-AP Quadrant Televentu | 0.2% | 46 | 7 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS55352 | FIVENET-IN Microscan Internet Limit | 0.2% | 170 | 40 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS131269 | CABLELITE-AS-AP Atria Convergence T | 0.2% | 30 | 1 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS150008 | PEL-AS-IN Pioneer Elabs Ltd. | 0.2% | 24 | 20 | 62.8% | **OK** — Compliant | Low | +0.1 pp |
| AS133287 | APSFL-AS Andhra Pradesh State Fiber | 0.2% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.2 pp |

### Archetype Key
| Code | Name | Policy Intervention |
|:----:|------|---------------------|
| A | Ghost (No Allocation) | Regulatory mandate for RIR membership / govt subsidy |
| C | Laggard (No Traffic) | Last Mile: CPE/router hardware import standards |
| D | **Bottleneck (High-Impact)** | **PRIORITY — Direct government engagement** |
| OK | Compliant | No immediate intervention required |

---

### IPv6 Deployment Age (Section 2.1.2)

| ASN | ISP | Market Share | Adoption | First IPv6 Seen | Age (yrs) | Reason |
|-----|-----|:-----------:|:--------:|:---------------:|:---------:|--------|
| AS55836 | RELIANCEJIO-IN Reliance Jio Infocomm Limited | 46.3% | 77.3% | 2012-12-10 | 13.5 | Top |
| AS45609 | BHARTI-MOBILITY-AS-AP Bharti Airtel Ltd. AS for GPRS Service | 22.0% | 69.7% | 2013-12-05 | 12.6 | Top |
| AS24560 | AIRTELBROADBAND-AS-AP Bharti Airtel Ltd., Telemedia Services | 8.3% | 65.4% | 2018-12-03 | 7.6 | Top |
| AS9829 | BSNL-NIB National Internet Backbone | 3.0% | 63.7% | 2009-06-29 | 17.0 | Top |
| AS38266 | VIL-AS-AP Vodafone Idea Ltd | 1.4% | 63.2% | 2016-01-24 | 10.4 | Top |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | N/A | — |
| 2021 | N/A | — |
| 2022 | N/A | — |
| 2023 | N/A | — |
| 2024 | N/A | — |

### Regional Position

- **IN adoption:** 78.4%
- **Global average:** 23.6%
- **Global rank:** #6 of 243 countries
- **vs Global Average:** +54.8 pp (above average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| AX | 79.3% | +0.9 pp |
| FK | 74.64% | -3.8 pp |
| FR | 83.31% | +4.9 pp |
| DE | 73.39% | -5.0 pp |
| SA | 72.85% | -5.6 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 835  
**IPv6-Reachable Domains:** 217  
**IPv4-Only Domains:** 618  
**IPv6 Web Readiness:** 26.00%  

> This analysis measures IPv6 reachability among
> ranked/popular domains within the national
> web ecosystem.

> Domains were classified as IPv6-capable when
> associated hostnames resolved to AF=6 IP nodes
> within the IYP graph.

> IPv4-only domains represent services that
> continue to rely exclusively on IPv4 connectivity.

### Government Website IPv6 Readiness

**Government Domains Assessed:** 947  
**IPv6-Capable Government Domains:** 125  
**IPv4-Only Government Domains:** 812  
**Government IPv6 Readiness:** 13.20%  

> Government domains were identified using
> the .gov.in namespace and evaluated for
> IPv6-capable hostname resolution.

> Results indicate comparatively weak IPv6
> adoption within public-sector digital
> infrastructure.



---

### Comparative Sector IPv6 Readiness

| Sector | Domains | IPv6 Readiness |
|--------|---------|----------------|
| Banking | 104 | 53.85% |
| News | 126 | 53.97% |
| Education | 474 | 39.45% |
| Ecommerce | 139 | 43.17% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 68  
**Self-Hosted Domains:** 932  
**IPv6-Capable CDN Domains:** 57  
**IPv4-Only Self-Hosted Domains:** 512  

> CDN infrastructure was inferred through
> hostname alias relationships associated
> with major CDN and edge-hosting providers.

> Results suggest that IPv6 deployment is
> significantly stronger among CDN-backed
> services than self-hosted infrastructure.

---

## Section 5 — Country TLD IPv6 Health

**Analyzed ccTLD:** .in  
**Domains Sampled:** 5000  
**IPv6-Enabled Domains:** 2045  
**IPv6 / AAAA Readiness:** 40.90%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .in | 40.90% |
| .com | 44.14% |
| .fr | 37.64% |
| .de | 39.34% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-06-05 | 5000 | 2045 | 40.9% |
| 2026-06-12 | 5000 | 2045 | 40.9% |
| 2026-06-26 | 5000 | 2045 | 40.9% |

> TLD IPv6 readiness has remained stable by 0.0 pp since 2026-06-05 (3 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 2062  
**IPv6-Reachable Nameservers:** 1135  
**IPv6 NS Reachability:** 55.04%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 136  
**IPv6-Capable Glue Nameservers:** 1  
**Glue IPv6 Readiness:** 0.74%  

> This approximation identifies in-zone authoritative
> nameservers whose hostnames fall within the same
> domain hierarchy as the delegated domain.

> Results suggest that IPv6 adoption among self-hosted
> authoritative DNS infrastructure remains limited
> within the sampled ccTLD ecosystem.

---

## Impact Formula Reference

```
A_new = A_nat + M_z × (1.0 - A_z)

  A_nat = national IPv6 adoption (0–1)
  M_z   = ISP market share (0–1, from APNIC population proxy)
  A_z   = ISP current IPv6 adoption estimate (0–1)
```

> Source: ISOC Internet Resilience Index Methodology, April 2025 v1.0
> Pillar: Enabling Technologies & Security (25%) → Enabling Technologies (20%) → IPv6 (30%)

---

*Report generated by ISOC Pulse × IYP IPv6 Policy Engine*  
*Team: Rahul Rajesh, Ron Prajoth, Aditya Menon | Mentor: Amreesh Phokeer (ISOC)*