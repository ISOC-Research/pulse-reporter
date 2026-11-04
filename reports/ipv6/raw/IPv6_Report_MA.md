# IPv6 Policy Brief — MA
**Generated:** 2026-11-04 11:43  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

MA currently has a national IPv6 adoption rate of 3.8%, with 99.9% of the subscriber market served by ISPs classified as non-compliant. PRIORITY ACTION — 2 high-impact bottleneck provider(s) identified: AS36903 (Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM, 62.7% market share): targeting this provider alone would increase national adoption from 3.8% to 64.0% (+60.2 percentage points); AS36925 (MEDITELECOM - MEDITELECOM, 33.1% market share): targeting this provider alone would increase national adoption from 3.8% to 35.7% (+31.9 percentage points). 4 ISP(s) (covering 4.1% of the market) have active BGP announcements but near-zero user-side adoption, indicating a last-mile CPE or hardware configuration problem requiring targeted equipment standards enforcement.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 120  
**RPKI-Covered Prefixes:** 41  
**RPKI Coverage:** 34.17%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| Office National des Postes et Telecommun | 68 | 0.00% |
| Office National des Postes et Telecommun | 10 | 0.00% |
| Wana Corporate - Wana Corporate | 1 | 0.00% |
| MEDITELECOM - MEDITELECOM | 37 | 100.00% |
| CNRST (Centre National pour la Recherche | 4 | 100.00% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 6  
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
| CAS-IX | No | 3 | 3 | 100.0% |
| FEZIX | No | 3 | 0 | 0.0% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 3.8%  
**Underserved Market Share:** 99.9%  
**ISPs Assessed:** 6

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS36903 | Office National des Postes et Telec | 62.7% | 204 | 1 | 4.0% | **D** — Bottleneck (High-Impact) | Low | +60.2 pp |
| AS36925 | MEDITELECOM - MEDITELECOM | 33.1% | 110 | 22 | 3.6% | **D** — Bottleneck (High-Impact) | Low | +31.9 pp |
| AS6713 | Office National des Postes et Telec | 2.9% | 30 | 21 | 3.1% | **C** — Laggard (No Traffic) | Low | +2.8 pp |
| AS36884 | Wana Corporate - Wana Corporate | 1.1% | 3 | 12 | 3.1% | **C** — Laggard (No Traffic) | Low | +1.0 pp |
| AS30983 | CNRST (Centre National pour la Rech | 0.1% | 10 | 1 | 3.1% | **C** — Laggard (No Traffic) | Low | +0.1 pp |
| AS212238 | CDNEXT Datacamp Limited | 0.0% | 2021 | 1 | 3.1% | **C** — Laggard (No Traffic) | Low | +0.0 pp |

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
| AS36903 | Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM | 62.7% | 4.0% | 2015-03-18 | 11.6 | Top |
| AS36925 | MEDITELECOM - MEDITELECOM | 33.1% | 3.6% | 2012-07-19 | 14.3 | Top |
| AS6713 | Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM | 2.9% | 3.1% | 2008-01-06 | 18.8 | Top |
| AS36884 | Wana Corporate - Wana Corporate | 1.1% | 3.1% | 2013-07-26 | 13.3 | Top |
| AS30983 | CNRST (Centre National pour la Recherche Scientifique et Technique) - CNRST (Centre National pour la Recherche Scientifique et Technique) | 0.1% | 3.1% | 2007-10-02 | 19.1 | Top |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | 1.0% | — |
| 2021 | 1.0% | +0.0 pp |
| 2022 | 1.0% | +0.0 pp |
| 2023 | 1.2% | +0.2 pp |
| 2024 | 1.2% | +0.0 pp |

### Regional Position

- **MA adoption:** 3.8%
- **Global average:** 24.4%
- **Global rank:** #187 of 243 countries
- **vs Global Average:** -20.6 pp (below average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| AQ | 3.87% | +0.1 pp |
| PA | 3.98% | +0.2 pp |
| ZM | 3.96% | +0.2 pp |
| ZA | 4.37% | +0.6 pp |
| MC | 3.31% | -0.5 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 883  
**IPv6-Reachable Domains:** 0  
**IPv4-Only Domains:** 883  
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

**Government Domains Assessed:** 34  
**IPv6-Capable Government Domains:** 7  
**IPv4-Only Government Domains:** 25  
**Government IPv6 Readiness:** 20.59%  

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
| Banking | 10 | 0.00% |
| News | 2 | 100.00% |
| Education | 2 | 50.00% |
| Ecommerce | 4 | 25.00% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 46  
**Self-Hosted Domains:** 511  
**IPv6-Capable CDN Domains:** 34  
**IPv4-Only Self-Hosted Domains:** 281  

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
**IPv6-Enabled Domains:** 1997  
**IPv6 / AAAA Readiness:** 39.94%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .ma | 39.94% |
| .com | 50.28% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-06-26 | 5000 | 1858 | 37.2% |
| 2026-11-04 | 5000 | 1997 | 39.9% |

> TLD IPv6 readiness has increased by 2.8 pp since 2026-06-26 (2 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 1432  
**IPv6-Reachable Nameservers:** 792  
**IPv6 NS Reachability:** 55.31%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 121  
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