# IPv6 Policy Brief — IN
**Generated:** 2026-11-04 10:31  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

IN currently has a national IPv6 adoption rate of 76.4%, with 0.0% of the subscriber market served by ISPs classified as non-compliant. All major ISPs are currently classified as compliant. Focus should shift to sustaining adoption growth and improving RPKI security hygiene.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 17,468  
**RPKI-Covered Prefixes:** 16,206  
**RPKI Coverage:** 92.78%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| TATAPLAYBROADBAND-AS-AP - TATA PLAY BROA | 627 | 0.00% |
| DNA-AS-AP - DIGITAL NETWORK ASSOCIATES P | 102 | 0.00% |
| FIVENET-IN - Microscan Internet Limited | 97 | 32.99% |
| BBIL-AP - BHARTI Airtel Ltd. | 160 | 52.50% |
| EXCITEL-AS-IN - Excitel Broadband Privat | 138 | 93.48% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 224  
**IPv6-Capable Upstream Reachability:** 100.00%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 40  
**IXPs with IPv6 LAN:** 34 (85.0%)  
**Members with IPv6 Peering:** 1508 / 1934 (78.0%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| DE-CIX Mumbai | Yes | 450 | 323 | 71.8% |
| Extreme IX Mumbai | Yes | 254 | 202 | 79.5% |
| Extreme IX Delhi | Yes | 182 | 142 | 78.0% |
| NIXI Mumbai | Yes | 180 | 149 | 82.8% |
| NIXI Delhi | Yes | 115 | 87 | 75.7% |
| DE-CIX Delhi | Yes | 103 | 78 | 75.7% |
| Extreme IX Chennai | Yes | 94 | 78 | 83.0% |
| DE-CIX Chennai | Yes | 76 | 56 | 73.7% |
| AMS-IX Mumbai | Yes | 75 | 58 | 77.3% |
| NIXI Chennai | Yes | 57 | 50 | 87.7% |
| Extreme IX Bangalore | Yes | 42 | 36 | 85.7% |
| ANI-IX Delhi | Yes | 30 | 15 | 50.0% |
| Kolkata IX | Yes | 29 | 27 | 93.1% |
| NIXI Kolkata | Yes | 29 | 26 | 89.7% |
| Extreme IX Kolkata | Yes | 26 | 24 | 92.3% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 76.4%  
**Underserved Market Share:** 0.0%  
**ISPs Assessed:** 25

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS55836 | RELIANCEJIO-IN - Reliance Jio Infoc | 47.2% | 5163 | 445 | 75.5% | **OK** — Compliant | High | +11.6 pp |
| AS45609 | BHARTI-MOBILITY-AS-AP - Bharti Airt | 22.8% | 10842 | 1 | 68.1% | **OK** — Compliant | Low | +7.3 pp |
| AS24560 | AIRTELBROADBAND-AS-AP - Bharti Airt | 9.0% | 1533 | 1 | 63.8% | **OK** — Compliant | Low | +3.2 pp |
| AS9829 | BSNL-NIB - National Internet Backbo | 2.8% | 3350 | 74 | 62.0% | **OK** — Compliant | Medium | +1.1 pp |
| AS133982 | EXCITEL-AS-IN - Excitel Broadband P | 0.9% | 357 | 8 | 61.4% | **OK** — Compliant | Low | +0.3 pp |
| AS24309 | CABLELITE-AS-AP - Atria Convergence | 0.9% | 342 | 14 | 61.4% | **OK** — Compliant | Low | +0.3 pp |
| AS133661 | NETPLUS-AS - Netplus Broadband Serv | 0.8% | 98 | 5 | 61.4% | **OK** — Compliant | Low | +0.3 pp |
| AS45916 | GTPL-AS-AP - Gujarat Telelink Pvt L | 0.8% | 854 | 10 | 61.3% | **OK** — Compliant | Low | +0.3 pp |
| AS138754 | KVBPL-AS-IN - Kerala Vision Broad B | 0.7% | 63 | 3 | 61.3% | **OK** — Compliant | Low | +0.3 pp |
| AS17488 | HATHWAY-NET-AP - Hathway IP Over Ca | 0.7% | 150 | 3 | 61.3% | **OK** — Compliant | Low | +0.3 pp |
| AS17665 | ONEBROADBAND - ONEOTT INTERTAINMENT | 0.5% | 308 | 91 | 61.3% | **OK** — Compliant | Medium | +0.2 pp |
| AS23860 | ALLIANCE-GATEWAY-AS-AP - Alliance B | 0.5% | 1011 | 6 | 61.2% | **OK** — Compliant | Low | +0.2 pp |
| AS55577 | CABLELITE-AS-AP - Atria Convergence | 0.5% | 150 | 1 | 61.2% | **OK** — Compliant | Low | +0.2 pp |
| AS24186 | RAILTEL-AS-IN - RailTel Corporation | 0.4% | 392 | 22 | 61.2% | **OK** — Compliant | Low | +0.2 pp |
| AS134674 | TATAPLAYBROADBAND-AS-AP - TATA PLAY | 0.4% | 1817 | 8 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS18209 | CABLELITE-AS-AP - Atria Convergence | 0.3% | 99 | 5 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS38266 | VIL-AS-AP - Vodafone Idea Ltd | 0.3% | 3833 | 1 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS55352 | FIVENET-IN - Microscan Internet Lim | 0.2% | 271 | 32 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS132116 | ANINETWORK-IN - Anonet Network Priv | 0.2% | 84 | 19 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS17917 | QTLTELECOM-AS-AP - Quadrant Televen | 0.2% | 69 | 9 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS17465 | ASIANET - Cable ISP in India | 0.2% | 72 | 6 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS150008 | PEL-AS-IN - Pioneer Elabs Ltd. | 0.2% | 36 | 19 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS131269 | CABLELITE-AS-AP - Atria Convergence | 0.2% | 48 | 1 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS138296 | STARNET7-AS - Juweriyah Networks Pr | 0.2% | 8 | 14 | 61.2% | **OK** — Compliant | Low | +0.1 pp |
| AS45769 | DVOIS-IN - D-Vois Broadband Pvt Ltd | 0.1% | 75 | 9 | 61.2% | **OK** — Compliant | Low | +0.1 pp |

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
| AS55836 | RELIANCEJIO-IN - Reliance Jio Infocomm Limited | 47.2% | 75.5% | 2012-12-10 | 13.9 | Top |
| AS45609 | BHARTI-MOBILITY-AS-AP - Bharti Airtel Ltd. AS for GPRS Service | 22.8% | 68.1% | 2013-12-05 | 12.9 | Top |
| AS24560 | AIRTELBROADBAND-AS-AP - Bharti Airtel Ltd., Telemedia Services | 9.0% | 63.8% | 2018-12-03 | 7.9 | Top |
| AS9829 | BSNL-NIB - National Internet Backbone | 2.8% | 62.0% | 2009-06-29 | 17.3 | Top |
| AS133982 | EXCITEL-AS-IN - Excitel Broadband Private Limited | 0.9% | 61.4% | 2018-08-17 | 8.2 | Top |

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

- **IN adoption:** 76.4%
- **Global average:** 24.4%
- **Global rank:** #5 of 243 countries
- **vs Global Average:** +52.0 pp (above average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| SA | 74.83% | -1.6 pp |
| DE | 72.95% | -3.5 pp |
| MY | 72.47% | -3.9 pp |
| BE | 72.02% | -4.4 pp |
| AX | 70.21% | -6.2 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 836  
**IPv6-Reachable Domains:** 0  
**IPv4-Only Domains:** 836  
**IPv6 Web Readiness:** 0.00%  

> This analysis measures IPv6 reachability among
> ranked/popular domains within the national
> web ecosystem.

> Domains were classified as IPv6-capable when
> associated hostnames resolved to AF=6 IP nodes
> within the IYP graph.

> IPv4-only domains represent services that
> continue to rely exclusively on IPv4 connectivity.

### Government Website IPv6 Readiness

**Government Domains Assessed:** 1000  
**IPv6-Capable Government Domains:** 165  
**IPv4-Only Government Domains:** 821  
**Government IPv6 Readiness:** 16.50%  

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
| Banking | 113 | 52.21% |
| News | 116 | 50.00% |
| Education | 587 | 40.03% |
| Ecommerce | 136 | 44.85% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 65  
**Self-Hosted Domains:** 935  
**IPv6-Capable CDN Domains:** 52  
**IPv4-Only Self-Hosted Domains:** 481  

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
**IPv6-Enabled Domains:** 2109  
**IPv6 / AAAA Readiness:** 42.18%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .in | 42.18% |
| .com | 50.28% |
| .fr | 39.50% |
| .de | 40.10% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-06-05 | 5000 | 2045 | 40.9% |
| 2026-06-12 | 5000 | 2045 | 40.9% |
| 2026-06-26 | 5000 | 2045 | 40.9% |
| 2026-07-10 | 5000 | 2045 | 40.9% |
| 2026-11-04 | 5000 | 2109 | 42.2% |

> TLD IPv6 readiness has increased by 1.3 pp since 2026-06-05 (5 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 2062  
**IPv6-Reachable Nameservers:** 1149  
**IPv6 NS Reachability:** 55.72%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 117  
**IPv6-Capable Glue Nameservers:** 0  
**Glue IPv6 Readiness:** 0.00%  

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