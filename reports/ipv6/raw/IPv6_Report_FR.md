# IPv6 Policy Brief — FR
**Generated:** 2026-11-04 11:22  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

FR currently has a national IPv6 adoption rate of 86.0%, with 0.0% of the subscriber market served by ISPs classified as non-compliant. All major ISPs are currently classified as compliant. Focus should shift to sustaining adoption growth and improving RPKI security hygiene.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 985  
**RPKI-Covered Prefixes:** 964  
**RPKI Coverage:** 97.87%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| ALPHALINK-AS Alphalink SASU | 7 | 71.43% |
| FLEXNETWORK-AS FLEX NETWORK SARL | 5 | 80.00% |
| BANDWIDTH-AS Hydra Communications Ltd | 19 | 89.47% |
| VELIANET-AS velia.net Internetdienste Gm | 10 | 90.00% |
| ZEN-DPS - Zenlayer Inc | 89 | 91.01% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 67  
**IPv6-Capable Upstream Reachability:** 100.00%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 27  
**IXPs with IPv6 LAN:** 26 (96.3%)  
**Members with IPv6 Peering:** 1334 / 1471 (90.7%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| France-IX Paris | Yes | 452 | 400 | 88.5% |
| Equinix Paris | Yes | 241 | 214 | 88.8% |
| nine | Yes | 140 | 133 | 95.0% |
| DE-CIX Marseille | Yes | 120 | 103 | 85.8% |
| France-IX Marseille | Yes | 110 | 106 | 96.4% |
| France-IX AURA | Yes | 74 | 62 | 83.8% |
| BGP.Exchange - Paris | Yes | 61 | 57 | 93.4% |
| Lillix | Yes | 46 | 45 | 97.8% |
| Hopus | Yes | 33 | 31 | 93.9% |
| BGP.Exchange - Lyon | Yes | 28 | 28 | 100.0% |
| SFINX | Yes | 24 | 21 | 87.5% |
| BreizhIX | Yes | 20 | 20 | 100.0% |
| France-IX Lille | Yes | 20 | 18 | 90.0% |
| ERA-IX Paris | Yes | 14 | 13 | 92.9% |
| AuvernIX | Yes | 13 | 13 | 100.0% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 86.0%  
**Underserved Market Share:** 0.0%  
**ISPs Assessed:** 25

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS3215 | AS3215 Orange S.A. | 36.2% | 135 | 179 | 81.3% | **OK** — Compliant | Medium | +6.8 pp |
| AS12322 | PROXAD Free SAS | 18.3% | 1581 | 4 | 75.1% | **OK** — Compliant | Low | +4.6 pp |
| AS5410 | BOUYGTEL-ISP Bouygues Telecom SA | 17.2% | 6 | 16 | 74.7% | **OK** — Compliant | Low | +4.3 pp |
| AS15557 | LDCOMNET Societe Francaise Du Radio | 16.7% | 36 | 88 | 74.6% | **OK** — Compliant | Medium | +4.2 pp |
| AS51207 | FREEM Free Mobile SAS | 5.0% | 3 | 1 | 70.5% | **OK** — Compliant | Low | +1.5 pp |
| AS12876 | AS12876 Scaleway SAS | 0.8% | 24 | 1 | 69.1% | **OK** — Compliant | Low | +0.3 pp |
| AS16276 | OVH OVH SAS | 0.8% | 126 | 172 | 69.1% | **OK** — Compliant | Medium | +0.2 pp |
| AS63023 | AS-GLOBALTELEHOST - GTHost | 0.7% | 106 | 52 | 69.0% | **OK** — Compliant | Medium | +0.2 pp |
| AS51167 | CONTABO Contabo GmbH | 0.6% | 15 | 1 | 69.0% | **OK** — Compliant | Low | +0.2 pp |
| AS13335 | CLOUDFLARENET - Cloudflare, Inc. | 0.5% | 8848 | 963 | 69.0% | **OK** — Compliant | High | +0.1 pp |
| AS14593 | SPACEX-STARLINK - Space Exploration | 0.3% | 2730 | 18 | 68.9% | **OK** — Compliant | Low | +0.1 pp |
| AS16509 | AMAZON-02 - Amazon.com, Inc. | 0.2% | 17385 | 88 | 68.9% | **OK** — Compliant | Medium | +0.1 pp |
| AS31404 | Lycatel-AS LYCATEL DISTRIBUTION UK  | 0.2% | 9 | 1 | 68.9% | **OK** — Compliant | Low | +0.1 pp |
| AS212238 | CDNEXT Datacamp Limited | 0.2% | 2021 | 1 | 68.9% | **OK** — Compliant | Low | +0.1 pp |
| AS52075 | WIFIRST Wifirst S.A.S. | 0.1% | 30 | 1 | 68.9% | **OK** — Compliant | Low | +0.0 pp |
| AS29066 | VELIANET-AS velia.net Internetdiens | 0.1% | 30 | 8 | 68.9% | **OK** — Compliant | Low | +0.0 pp |
| AS16347 | INHERENT ADISTA SAS | 0.1% | 54 | 23 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS199636 | FREEBOXPRO Free Pro SAS | 0.1% | 3 | 1 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS62610 | ZEN-DPS - Zenlayer Inc | 0.1% | 256 | 44 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS63949 | AKAMAI-LINODE-AP - Akamai Connected | 0.1% | 291 | 1 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS42487 | Vialis-Moselle Vialis SEM | 0.1% | 21 | 2 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS8362 | NordNet SA | 0.1% | 3 | 1 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS8399 | SEWAN-FR SEWAN SAS | 0.1% | 12 | 1 | 68.8% | **OK** — Compliant | Low | +0.0 pp |
| AS174 | COGENT-174 - Cogent Communications, | 0.1% | 1417 | 41127 | 68.8% | **OK** — Compliant | Critical | +0.0 pp |
| AS136787 | PACKETHUBSA-AS-AP - PacketHub S.A. | 0.1% | 9 | 2 | 68.8% | **OK** — Compliant | Low | +0.0 pp |

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
| AS3215 | AS3215 Orange S.A. | 36.2% | 81.3% | 2009-04-18 | 17.5 | Top |
| AS12322 | PROXAD Free SAS | 18.3% | 75.1% | 2007-11-19 | 19.0 | Top |
| AS5410 | BOUYGTEL-ISP Bouygues Telecom SA | 17.2% | 74.7% | 2007-04-05 | 19.6 | Top |
| AS15557 | LDCOMNET Societe Francaise Du Radiotelephone - SFR SA | 16.7% | 74.6% | 2008-05-05 | 18.5 | Top |
| AS51207 | FREEM Free Mobile SAS | 5.0% | 70.5% | 2020-04-08 | 6.6 | Top |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | 70.4% | — |
| 2021 | 71.9% | +1.5 pp |
| 2022 | 92.1% | +20.2 pp |
| 2023 | 87.4% | -4.7 pp |
| 2024 | 88.5% | +1.1 pp |

### Regional Position

- **FR adoption:** 86.0%
- **Global average:** 24.4%
- **Global rank:** #4 of 243 countries
- **vs Global Average:** +61.6 pp (above average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| UM | 88.31% | +2.3 pp |
| IN | 76.38% | -9.6 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 761  
**IPv6-Reachable Domains:** 0  
**IPv4-Only Domains:** 761  
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

**Government Domains Assessed:** 144  
**IPv6-Capable Government Domains:** 33  
**IPv4-Only Government Domains:** 109  
**Government IPv6 Readiness:** 22.92%  

> Government domains were identified using
> the .gouv.fr namespace and evaluated for
> IPv6-capable hostname resolution.

> Results indicate comparatively weak IPv6
> adoption within public-sector digital
> infrastructure.



---

### Comparative Sector IPv6 Readiness

| Sector | Domains | IPv6 Readiness |
|--------|---------|----------------|
| Banking | 31 | 38.71% |
| News | 78 | 43.59% |
| Education | 70 | 47.14% |
| Ecommerce | 109 | 56.88% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 129  
**Self-Hosted Domains:** 871  
**IPv6-Capable CDN Domains:** 111  
**IPv4-Only Self-Hosted Domains:** 453  

> CDN infrastructure was inferred through
> hostname alias relationships associated
> with major CDN and edge-hosting providers.

> Results suggest that IPv6 deployment is
> significantly stronger among CDN-backed
> services than self-hosted infrastructure.

---

## Section 5 — Country TLD IPv6 Health

**Analyzed ccTLD:** .fr  
**Domains Sampled:** 5000  
**IPv6-Enabled Domains:** 1975  
**IPv6 / AAAA Readiness:** 39.50%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .fr | 39.50% |
| .com | 50.28% |
| .de | 40.10% |
| .in | 42.18% |

> Comparative sampled analysis across major TLD ecosystems
> provides relative benchmarking of IPv6 DNS readiness.

### TLD IPv6 Readiness Trend

| Date | Domains Sampled | IPv6-Enabled | Readiness |
|------|:---------------:|:------------:|:---------:|
| 2026-06-03 | 5000 | 1882 | 37.6% |
| 2026-06-05 | 5000 | 1882 | 37.6% |
| 2026-06-08 | 5000 | 1882 | 37.6% |
| 2026-06-12 | 5000 | 1882 | 37.6% |
| 2026-07-10 | 5000 | 1882 | 37.6% |
| 2026-09-13 | 5000 | 1975 | 39.5% |
| 2026-11-04 | 5000 | 1975 | 39.5% |

> TLD IPv6 readiness has increased by 1.9 pp since 2026-06-03 (7 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 1787  
**IPv6-Reachable Nameservers:** 1450  
**IPv6 NS Reachability:** 81.14%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 30  
**IPv6-Capable Glue Nameservers:** 11  
**Glue IPv6 Readiness:** 36.67%  

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