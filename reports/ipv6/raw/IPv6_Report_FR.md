# IPv6 Policy Brief — FR
**Generated:** 2026-07-10 02:27  
**Data Sources:** ISOC Pulse API 2024 · Internet Yellow Pages (IYP) Neo4j  
**Framework:** ISOC Internet Resilience Index — Security Pillar (Enabling Technologies)

---

## Executive Summary

FR currently has a national IPv6 adoption rate of 83.1%, with 0.0% of the subscriber market served by ISPs classified as non-compliant. All major ISPs are currently classified as compliant. Focus should shift to sustaining adoption growth and improving RPKI security hygiene.

---

## Section 1 — Core Infrastructure / RPKI Security

**Total IPv6 Prefixes:** 14,189  
**RPKI-Covered Prefixes:** 5,049  
**RPKI Coverage:** 35.58%  

> RPKI coverage measures the percentage of IPv6 routing prefixes
> protected using Route Origin Authorization (ROA) records for routing security.

---

### ISPs with Weak RPKI Coverage

| ISP | IPv6 Prefixes | RPKI Coverage |
|-----|---------------|---------------|
| PROXAD Free SAS | 527 | 0.57% |
| SPACEX-STARLINK - Space Exploration Tech | 776 | 0.77% |
| COGENT-174 - Cogent Communications, LLC | 567 | 6.00% |
| LEVEL3 - Level 3 Parent, LLC | 165 | 7.27% |
| ZEN-ECN | 149 | 11.41% |

> Several major networks continue to exhibit weak RPKI
> adoption despite significant IPv6 routing presence.

---

### Preliminary IPv6 Upstream Connectivity

**ISPs Assessed:** 65  
**IPv6-Capable Upstream Reachability:** 100.00%  

> Preliminary graph-based analysis suggests that most assessed
> ISPs maintain upstream dependencies connected to IPv6-capable
> transit or peering networks.

> NOTE: This metric is currently experimental and based on
> inferred AS dependency relationships within the IYP graph.

---

### IXP IPv6 Peering

**Domestic IXPs:** 25  
**IXPs with IPv6 LAN:** 24 (96.0%)  
**Members with IPv6 Peering:** 1217 / 1345 (90.5%)  

| IXP | IPv6 LAN | Members | IPv6 Members | IPv6 % |
|-----|:--------:|:-------:|:------------:|:------:|
| France-IX Paris | Yes | 447 | 397 | 88.8% |
| Equinix Paris | Yes | 243 | 214 | 88.1% |
| DE-CIX Marseille | Yes | 122 | 105 | 86.1% |
| France-IX Marseille | Yes | 112 | 108 | 96.4% |
| nine | Yes | 79 | 76 | 96.2% |
| France-IX AURA | Yes | 74 | 62 | 83.8% |
| BGP.Exchange - Paris | Yes | 44 | 41 | 93.2% |
| Lillix | Yes | 40 | 39 | 97.5% |
| Hopus | Yes | 33 | 30 | 90.9% |
| SFINX | Yes | 24 | 21 | 87.5% |
| BGP.Exchange - Lyon | Yes | 24 | 24 | 100.0% |
| BreizhIX | Yes | 20 | 20 | 100.0% |
| France-IX Lille | Yes | 16 | 15 | 93.8% |
| AuvernIX | Yes | 13 | 13 | 100.0% |
| France-IX Toulouse | Yes | 13 | 13 | 100.0% |

> IXP IPv6 readiness was measured using PeeringDB data within the IYP graph.

---

## Section 2 — ISP Compliance Scorecard

**National IPv6 Adoption:** 83.1%  
**Underserved Market Share:** 0.0%  
**ISPs Assessed:** 25

| ASN | ISP | Market Share | IPv6 Prefixes | Cone Size | Adoption Est. | Archetype | Severity | Proj. Impact |
|-----|-----|:------------:|:-------------:|:---------:|:-------------:|:---------:|:--------:|:------------:|
| AS3215 | AS3215 Orange S.A. | 35.4% | 86 | 203 | 78.2% | **OK** — Compliant | High | +7.7 pp |
| AS12322 | PROXAD Free SAS | 18.6% | 1054 | 4 | 72.7% | **OK** — Compliant | Low | +5.1 pp |
| AS5410 | BOUYGTEL-ISP Bouygues Telecom SA | 17.8% | 4 | 16 | 72.4% | **OK** — Compliant | Low | +4.9 pp |
| AS15557 | LDCOMNET Societe Francaise Du Radio | 17.5% | 24 | 91 | 72.3% | **OK** — Compliant | Medium | +4.8 pp |
| AS51207 | FREEM Free Mobile SAS | 4.5% | 2 | 1 | 68.0% | **OK** — Compliant | Low | +1.5 pp |
| AS16276 | OVH OVH SAS | 0.8% | 82 | 119 | 66.8% | **OK** — Compliant | Medium | +0.3 pp |
| AS63023 | AS-GLOBALTELEHOST - GTHost | 0.8% | 50 | 23 | 66.7% | **OK** — Compliant | Low | +0.3 pp |
| AS12876 | AS12876 Scaleway SAS | 0.7% | 14 | 1 | 66.7% | **OK** — Compliant | Low | +0.2 pp |
| AS51167 | CONTABO Contabo GmbH | 0.3% | 10 | 1 | 66.6% | **OK** — Compliant | Low | +0.1 pp |
| AS31404 | Lycatel-AS LYCATEL DISTRIBUTION UK  | 0.3% | 6 | 1 | 66.6% | **OK** — Compliant | Low | +0.1 pp |
| AS13335 | CLOUDFLARENET - Cloudflare, Inc. | 0.2% | 6208 | 922 | 66.5% | **OK** — Compliant | High | +0.1 pp |
| AS30058 | FDCSERVERS - FDCservers.net | 0.2% | 295 | 43 | 66.5% | **OK** — Compliant | Low | +0.1 pp |
| AS14593 | SPACEX-STARLINK - Space Exploration | 0.2% | 1511 | 14 | 66.5% | **OK** — Compliant | Low | +0.1 pp |
| AS21859 | ZEN-ECN | 0.2% | 291 | 398 | 66.5% | **OK** — Compliant | High | +0.1 pp |
| AS29066 | VELIANET-AS velia.net Internetdiens | 0.1% | 20 | 7 | 66.5% | **OK** — Compliant | Low | +0.1 pp |
| AS16509 | AMAZON-02 - Amazon.com, Inc. | 0.1% | 11016 | 75 | 66.5% | **OK** — Compliant | Medium | +0.1 pp |
| AS52075 | WIFIRST Wifirst S.A.S. | 0.1% | 16 | 1 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS62610 | ZEN-DPS - Zenlayer Inc | 0.1% | 158 | 11 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS212238 | CDNEXT Datacamp Limited | 0.1% | 975 | 1 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS136787 | PACKETHUBSA-AS-AP PacketHub S.A. | 0.1% | 6 | 1 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS2200 | FR-RENATER Reseau National de telec | 0.1% | 4 | 49 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS199636 | FREEBOXPRO Free Pro SAS | 0.1% | 2 | 1 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS42487 | Vialis-Moselle Vialis SEM | 0.1% | 14 | 2 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS63949 | AKAMAI-LINODE-AP Akamai Connected C | 0.1% | 191 | 1 | 66.5% | **OK** — Compliant | Low | +0.0 pp |
| AS16347 | INHERENT ADISTA SAS | 0.1% | 36 | 23 | 66.5% | **OK** — Compliant | Low | +0.0 pp |

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
| AS3215 | AS3215 Orange S.A. | 35.4% | 78.2% | 2009-04-18 | 17.2 | Top |
| AS12322 | PROXAD Free SAS | 18.6% | 72.7% | 2007-11-19 | 18.6 | Top |
| AS5410 | BOUYGTEL-ISP Bouygues Telecom SA | 17.8% | 72.4% | 2007-04-05 | 19.3 | Top |
| AS15557 | LDCOMNET Societe Francaise Du Radiotelephone - SFR SA | 17.5% | 72.3% | 2008-05-05 | 18.2 | Top |
| AS51207 | FREEM Free Mobile SAS | 4.5% | 68.0% | 2020-04-08 | 6.3 | Top |

> Source: [RIPEstat](https://stat.ripe.net) — Announced Prefixes endpoint (historical data from 2000–present).  
> ⭐ Top = queried due to high market share | ⚠ Laggard = queried due to low adoption despite significant market share

---

## Section 3 — User-Side Adoption

### Adoption Trend

| Year | IPv6 Adoption | Change |
|------|:-------------:|:------:|
| 2020 | 67.7% | — |
| 2021 | 71.9% | +4.2 pp |
| 2022 | 89.1% | +17.3 pp |
| 2023 | 87.0% | -2.2 pp |
| 2024 | 86.9% | -0.1 pp |

### Regional Position

- **FR adoption:** 83.1%
- **Global average:** 23.6%
- **Global rank:** #3 of 243 countries
- **vs Global Average:** +59.5 pp (above average)

**Closest peer countries by adoption score:**

| Country | Adoption | Gap |
|---------|:--------:|:---:|
| SH | 83.3% | +0.2 pp |
| FK | 79.85% | -3.2 pp |
| IN | 78.94% | -4.2 pp |
| PN | 77.78% | -5.3 pp |
| AX | 74.89% | -8.2 pp |

---

## Section 4 — Web Services IPv6 Readiness

**Popular Domains Analyzed:** 0  
**IPv6-Reachable Domains:** 0  
**IPv4-Only Domains:** 0  
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

**Government Domains Assessed:** 152  
**IPv6-Capable Government Domains:** 33  
**IPv4-Only Government Domains:** 118  
**Government IPv6 Readiness:** 21.71%  

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
| Banking | 25 | 48.00% |
| News | 117 | 29.91% |
| Education | 84 | 36.90% |
| Ecommerce | 93 | 58.06% |

> Comparative sectoral analysis highlights
> differences in IPv6 deployment maturity
> across major digital-service ecosystems.


---

### CDN Correlation and Hosting Analysis

**CDN-Backed Domains:** 128  
**Self-Hosted Domains:** 872  
**IPv6-Capable CDN Domains:** 109  
**IPv4-Only Self-Hosted Domains:** 455  

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
**IPv6-Enabled Domains:** 1882  
**IPv6 / AAAA Readiness:** 37.64%  

> Sample-based analysis of the national ccTLD ecosystem
> indicates the proportion of domains resolving to
> IPv6-capable infrastructure.

> IPv6 capability was inferred through hostname resolution
> to IP nodes with address family AF=6 within the IYP graph.


### Comparative TLD IPv6 Readiness

| TLD | IPv6 Readiness |
|------|----------------|
| .fr | 37.64% |
| .com | 44.14% |
| .de | 39.34% |
| .in | 40.90% |

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

> TLD IPv6 readiness has remained stable by 0.0 pp since 2026-06-03 (5 snapshots recorded).

### Authoritative Nameserver IPv6 Reachability

**Nameservers Assessed:** 1807  
**IPv6-Reachable Nameservers:** 1446  
**IPv6 NS Reachability:** 80.02%  

> This metric measures whether authoritative DNS
> infrastructure supporting the ccTLD ecosystem
> is directly reachable over IPv6.

> Nameserver IPv6 capability was inferred through
> RESOLVES_TO relationships toward AF=6 IP nodes
> within the IYP graph.

---

### Glue Record IPv6 Readiness

**Glue-style Nameservers Assessed:** 27  
**IPv6-Capable Glue Nameservers:** 5  
**Glue IPv6 Readiness:** 18.52%  

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