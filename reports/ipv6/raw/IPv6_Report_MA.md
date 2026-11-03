# IPv6 Policy Brief — MA
**Generated:** 2026-06-26 08:18  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

MA currently has a national IPv6 adoption rate of 2.1%, with 100.0% of the subscriber market served by ISPs classified as non-compliant. PRIORITY ACTION — 2 high-impact bottleneck provider(s) identified: AS36903 (MT-MPLS, 61.3% market share): targeting this provider alone would increase national adoption from 2.1% to 62.1% (+60.0 percentage points); AS36925 (ASMedi, 31.0% market share): targeting this provider alone would increase national adoption from 2.1% to 32.5% (+30.4 percentage points). 5 ISP(s) (covering 7.6% of the market) have active BGP announcements but near-zero user-side adoption, indicating a last-mile CPE or hardware configuration problem requiring targeted equipment standards enforcement.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 3,855  
**RPKI-Covered Prefixes:** 1,740  
**RPKI Coverage:** 45.14%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| MT-MPLS | 68 | 0.00% |
| ASMedi | 37 | 0.00% |
| IAM-AS | 10 | 0.00% |
| MAROCCONNECT | 1 | 0.00% |
| MARWAN-AS | 4 | 25.00% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 7  
**IPv6-Capable Upstream Reachability:** 100.00%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 2  
**IXPs with IPv6 LAN:** 0 (0.0%)  
**Members with IPv6 Peering:** 3 / 6 (50.0%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| FEZIX | No | 3 | 0 | 0.0% |
| CAS-IX | No | 3 | 3 | 100.0% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 2.1%  
**Underserved Market Share:** 100.0%  
**ISPs Assessed:** 7

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS36903 | MT-MPLS | 61.3% | 136 | 1 | 2.2% | **D** — Bottleneck (High-Impact) | Low | +60.0 pp |
| AS36925 | ASMedi | 31.0% | 74 | 19 | 1.9% | **D** — Bottleneck (High-Impact) | Low | +30.4 pp |
| AS6713 | IAM-AS | 6.3% | 20 | 16 | 1.7% | **C** — Laggard (No Traffic) | Low | +6.2 pp |
| AS36884 | MAROCCONNECT | 1.0% | 2 | 10 | 1.7% | **C** — Laggard (No Traffic) | Low | +1.0 pp |
| AS30983 | MARWAN-AS | 0.2% | 7 | 1 | 1.7% | **C** — Laggard (No Traffic) | Low | +0.2 pp |
| AS13335 | CLOUDFLARENET - Cloudflare, Inc. | 0.1% | 6208 | 922 | 1.7% | **C** — Laggard (No Traffic) | High | +0.1 pp |
| AS212238 | CDNEXT Datacamp Limited | 0.0% | 975 | 1 | 1.7% | **C** — Laggard (No Traffic) | Low | +0.0 pp |

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
| AS36903 | MT-MPLS | 61.3% | 2.2% | 2015-03-18 | 11.3 | Top |
| AS36925 | ASMedi | 31.0% | 1.9% | 2012-07-19 | 13.9 | Top |
| AS6713 | IAM-AS | 6.3% | 1.7% | 2008-01-06 | 18.5 | Top |
| AS36884 | MAROCCONNECT | 1.0% | 1.7% | 2013-07-26 | 12.9 | Top |
| AS30983 | MARWAN-AS | 0.2% | 1.7% | 2007-10-02 | 18.7 | Top |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | 0.0% | — |
| 2021 | 0.0% | +0.0 pp |
| 2022 | 0.0% | +0.0 pp |
| 2023 | 0.2% | +0.2 pp |
| 2024 | 0.2% | +0.1 pp |

### Regional Position

- **MA adoption:** 2.1%
- **Global average:** 23.6%
- **Global rank:** #190 of 243 countries
- **vs Global Average:** -21.5 pp (below average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| ST | 2.19% | +0.1 pp |
| RU | 2.32% | +0.2 pp |
| CM | 2.28% | +0.2 pp |
| SZ | 2.28% | +0.2 pp |
| UG | 1.87% | -0.2 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 878  
**IPv6-Reachable Domains:** 231  
**IPv4-Only Domains:** 647  
**IPv6 Web Readiness:** 26.30%  

> This analysis measures IPv6 reachability among
> ranked/popular domains within the national
> web ecosystem.

> Domains were classified as IPv6-capable when
> associated hostnames resolved to AF=6 IP nodes
> within the IYP graph.

> IPv4-only domains represent services that
> continue to rely exclusively on IPv4 connectivity.

### Government Website IPv6 Readiness

**Government Domains Assessed:** 32  
**IPv6-Capable Government Domains:** 5  
**IPv4-Only Government Domains:** 27  
**Government IPv6 Readiness:** 15.62%  

> Government domains were identified using
> the .gov.ma namespace and evaluated for
> IPv6-capable hostname resolution.

> Results indicate comparatively weak IPv6
> adoption within public-sector digital
> infrastructure.



---

### Comparative Sector IPv6 Readiness

| Sector | Domains | IPv6 Readiness |
|--------|---------|----------------|
| Banking | 11 | 0.00% |
| News | 5 | 100.00% |
| Education | 2 | 50.00% |
| Ecommerce | 4 | 50.00% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 41  
**Self-Hosted Domains:** 467  
**IPv6-Capable CDN Domains:** 28  
**IPv4-Only Self-Hosted Domains:** 284  

> CDN infrastructure was inferred through
> hostname alias relationships associated
> with major CDN and edge-hosting providers.

> Results suggest that IPv6 deployment is
> significantly stronger among CDN-backed
> services than self-hosted infrastructure.

---

## Section 5 — Country TLD IPv6 Health

**Analyzed ccTLD:** .ma  
**Domains Sampled:** 5000  
**IPv6-Enabled Domains:** 1858  
**IPv6 / AAAA Readiness:** 37.16%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .ma | 37.16% |
| .com | 44.14% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-06-26 | 5000 | 1858 | 37.2% |

> This is the first recorded snapshot. Run the report again in the future to build a trend.

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 1453  
**IPv6-Reachable Nameservers:** 741  
**IPv6 NS Reachability:** 51.00%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 147  
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