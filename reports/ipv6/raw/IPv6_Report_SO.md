# IPv6 Policy Brief — SO
**Generated:** 2026-11-04 11:30  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

SO currently has a national IPv6 adoption rate of 0.5%, with 100.0% of the subscriber market served by ISPs classified as non-compliant. PRIORITY ACTION — 2 high-impact bottleneck provider(s) identified: AS37371 (Hormuud Telecom Somalia INC - Hormuud Telecom Somalia INC, 42.9% market share): targeting this provider alone would increase national adoption from 0.5% to 43.4% (+42.9 percentage points); AS37473 (Telesom - Telesom, 18.4% market share): targeting this provider alone would increase national adoption from 0.5% to 18.8% (+18.3 percentage points). 11 ISP(s) (covering 36.2% of the market) have zero IPv6 prefixes in the global routing table and require immediate regulatory intervention for RIR membership. 2 ISP(s) (covering 2.4% of the market) have active BGP announcements but near-zero user-side adoption, indicating a last-mile CPE or hardware configuration problem requiring targeted equipment standards enforcement.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 19  
**RPKI-Covered Prefixes:** 19  
**RPKI Coverage:** 100.00%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| Telesom - Telesom | 18 | 100.00% |
| SomCable - SomCable | 1 | 100.00% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 15  
**IPv6-Capable Upstream Reachability:** 100.00%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 1  
**IXPs with IPv6 LAN:** 1 (100.0%)  
**Members with IPv6 Peering:** 0 / 0 (0.0%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| SoIXP | Yes | 0 | 0 | 0.0% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 0.5%  
**Underserved Market Share:** 100.0%  
**ISPs Assessed:** 15

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS37371 | Hormuud Telecom Somalia INC - Hormu | 42.9% | 0 | 5 | 0.0% | **D** — Bottleneck (High-Impact) | Low | +42.9 pp |
| AS37473 | Telesom - Telesom | 18.4% | 54 | 1 | 0.4% | **D** — Bottleneck (High-Impact) | Low | +18.3 pp |
| AS37563 | SOMTEL INTERNATIONAL Ltd - SOMTEL I | 11.5% | 0 | 2 | 0.0% | **A** — Ghost (No Allocation) | Low | +11.5 pp |
| AS328250 | Golis Telecom Somalia - Golis Telec | 11.3% | 0 | 6 | 0.0% | **A** — Ghost (No Allocation) | Low | +11.3 pp |
| AS328469 | Somtel Somalia LTD - Somtel Somalia | 7.7% | 0 | 5 | 0.0% | **A** — Ghost (No Allocation) | Low | +7.7 pp |
| AS328319 | AMTEL LTD - AMTEL LTD | 2.2% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +2.2 pp |
| AS37425 | SomCable - SomCable | 2.0% | 3 | 7 | 0.4% | **C** — Laggard (No Traffic) | Low | +2.0 pp |
| AS328959 | SO! Limited - SO! Limited | 1.9% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +1.9 pp |
| AS328954 | BL27-AS | 0.6% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.6 pp |
| AS328590 | Somlink Wireless Network - Somlink  | 0.5% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.5 pp |
| AS14593 | SPACEX-STARLINK - Space Exploration | 0.4% | 2730 | 18 | 0.4% | **C** — Laggard (No Traffic) | Low | +0.4 pp |
| AS327828 | Somali-Optical-Networks | 0.3% | 0 | 2 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.3 pp |
| AS327768 | Somcast Networks LLC - Somcast Netw | 0.1% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.1 pp |
| AS327742 | SOMALI-WIRELESS | 0.1% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.1 pp |
| AS328953 | TAYOCOM | 0.1% | 0 | 1 | 0.0% | **A** — Ghost (No Allocation) | Low | +0.1 pp |

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
| AS37371 | Hormuud Telecom Somalia INC - Hormuud Telecom Somalia INC | 42.9% | 0.0% | N/A | N/A | Top |
| AS37473 | Telesom - Telesom | 18.4% | 0.4% | 2022-12-18 | 3.9 | Top |
| AS37563 | SOMTEL INTERNATIONAL Ltd - SOMTEL INTERNATIONAL Ltd | 11.5% | 0.0% | N/A | N/A | Top |
| AS328250 | Golis Telecom Somalia - Golis Telecom Somalia | 11.3% | 0.0% | N/A | N/A | Top |
| AS328469 | Somtel Somalia LTD - Somtel Somalia LTD | 7.7% | 0.0% | N/A | N/A | Top |
| AS328319 | AMTEL LTD - AMTEL LTD | 2.2% | 0.0% | N/A | N/A | Laggard |
| AS37425 | SomCable - SomCable | 2.0% | 0.4% | 2022-12-30 | 3.8 | Laggard |
| AS328959 | SO! Limited - SO! Limited | 1.9% | 0.0% | N/A | N/A | Laggard |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | 1.0% | — |
| 2021 | 1.0% | +0.0 pp |
| 2022 | 1.2% | +0.2 pp |
| 2023 | 1.6% | +0.4 pp |
| 2024 | 1.4% | -0.3 pp |

### Regional Position

- **SO adoption:** 0.5%
- **Global average:** 24.4%
- **Global rank:** #216 of 243 countries
- **vs Global Average:** -23.9 pp (below average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| KH | 0.48% | -0.0 pp |
| LB | 0.48% | -0.0 pp |
| PS | 0.58% | +0.1 pp |
| TZ | 0.55% | +0.1 pp |
| AZ | 0.42% | -0.1 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 172  
**IPv6-Reachable Domains:** 0  
**IPv4-Only Domains:** 172  
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

**Government Domains Assessed:** 4  
**IPv6-Capable Government Domains:** 3  
**IPv4-Only Government Domains:** 1  
**Government IPv6 Readiness:** 75.00%  

> Government domains were identified using
> the .gov.so namespace and evaluated for
> IPv6-capable hostname resolution.

> Results indicate comparatively weak IPv6
> adoption within public-sector digital
> infrastructure.



---

### Comparative Sector IPv6 Readiness

| Sector | Domains | IPv6 Readiness |
|--------|---------|----------------|
| Banking | 1 | 0.00% |
| News | 1 | 0.00% |
| Education | 2 | 0.00% |
| Ecommerce | 0 | 0.00% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 20  
**Self-Hosted Domains:** 156  
**IPv6-Capable CDN Domains:** 15  
**IPv4-Only Self-Hosted Domains:** 58  

> CDN infrastructure was inferred through
> hostname alias relationships associated
> with major CDN and edge-hosting providers.

> Results suggest that IPv6 deployment is
> significantly stronger among CDN-backed
> services than self-hosted infrastructure.

---

## Section 5 — Country TLD IPv6 Health

**Analyzed ccTLD:** .so  
**Domains Sampled:** 732  
**IPv6-Enabled Domains:** 374  
**IPv6 / AAAA Readiness:** 51.09%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .so | 51.09% |
| .com | 50.28% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-09-17 | 732 | 374 | 51.1% |
| 2026-11-04 | 732 | 374 | 51.1% |

> TLD IPv6 readiness has remained stable by 0.0 pp since 2026-09-17 (2 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 1009  
**IPv6-Reachable Nameservers:** 816  
**IPv6 NS Reachability:** 80.87%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 12  
**IPv6-Capable Glue Nameservers:** 8  
**Glue IPv6 Readiness:** 66.67%  

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