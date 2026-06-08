# YPI Cypher Queries — Complete Reference

> All Cypher queries used for the IYP research, organized by pillar, sub-category, and metric. Each query is numbered in execution order. All outputs shown are for **France (`FR`)**.

# 1. Infrastructure

## 1.1 Enabling Infrastructure

### 1.1.1 Data Center Coverage

**Query 1 — Data center facilities and colocated ASes**

```cypher
// Lists all data center facilities (colocation facilities) in a country,
// along with the count of ASes colocated at each facility.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (f:Facility)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (a:AS)-[:LOCATED_IN]->(f)
RETURN f.name AS DataCenter, COUNT(DISTINCT a) AS ColocatedASes
ORDER BY ColocatedASes DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Data Center Facility Landscape in FR

This analysis maps all physical data center (colocation) facilities registered in the country via PeeringDB, ranked by how many Autonomous Systems are colocated at each site. High colocation density at a facility indicates it is a critical hub for the country's internet infrastructure.
g

**Data Centers by Colocated Network Count:**

| Data Center Name | Colocated ASes |
|------------------|----------------|

| Telehouse - Paris 2 (Voltaire - Léon Frot) | 347 |

| Digital Realty Marseille MRS1/2/3/4 | 212 |

| Equinix PA2 - Paris, Saint-Denis | 141 |

| Equinix PA3 - Paris, Saint-Denis | 120 |

| UltraEdge Lyon-Venissieux | 82 |

| Digital Realty Paris PAR5 | 68 |

| Equinix PA6 - Paris, Condorcet | 56 |

| Equinix PA5 - Paris, Victor Hugo | 55 |

| Digital Realty Paris PAR2 | 53 |

| Equinix PA7 - Paris, Energy Park | 49 |

| Telehouse - Paris 3 (Magny) | 48 |

| OPCORE - DC2 / PAR2 | 47 |

| Equinix PA4 - Paris, Pantin | 47 |

| ETIX Lille #2 | 46 |

| UltraEdge Paris - Courbevoie | 41 |

| UltraEdge Strasbourg | 41 |

| Digital Realty Paris PAR1 | 34 |

| Global Switch Paris | 31 |

| UltraEdge Bordeaux | 28 |

| ETIX Lyon #1 | 27 |

| Free Pro - Marseille - MRS1 | 27 |

| Cogent Rennes | 26 |

| OPCORE - DC3 / PAR3 | 25 |

| Free Pro - Lyon - Rock | 23 |

| Cogent Grenoble | 21 |

| DATA4 Paris Marcoussis - PAR1 | 21 |

| Eurofiber DC - TLS00 | 21 |

| Digital Realty Paris PAR7 | 20 |

| Treefaz Jeûneurs | 20 |

| ETIX Lille #3 | 20 |

| ETIX Nantes #1 | 20 |

| dc2scale PAR2 (Vélizy-Villacoublay) | 20 |

| Telehouse - Paris 1 (Jeûneurs) | 19 |

| nLighten Lyon LYS1 | 19 |

| Digital Realty Paris PAR3 | 18 |

| Cogent Toulouse | 18 |

| Cogent Nantes | 17 |

| Free Pro - Limonest | 16 |

| Orange Business - La Fabrique [Grenoble] | 15 |

| nLighten Sophia Antipolis NCE1 | 15 |

| Cogent Montpellier | 15 |

| Equinix PA10 - Paris, Saint-Denis | 14 |

| Digital Realty Paris PAR6 | 14 |

| ETIX Lille #1 | 13 |

| nLighten Besancon MLH1 | 13 |

| Level(3) Paris (Le Capitole) | 12 |

| Penta Infra Paris PAR01 | 12 |

| ETIX Nantes #2 | 12 |

| Telco Center | 12 |

| ETIX Montpellier #1 | 12 |

| Cogent Strasbourg | 12 |

| dc2scale PAR3 (Vélizy-Villacoublay) | 11 |

| ETIX Toulouse #1 | 11 |

| Cogent Bordeaux | 11 |

| Cogent Poitiers | 10 |

| TDF Datacenter Rennes Cesson | 10 |

| Cogent Dijon | 10 |

| CC IN2P3 | 10 |

| Cogent Rouen | 9 |

| Oceanet Armor B | 9 |

| Ikoula IKDC1 | 9 |

| Datacenter NEXEREN | 8 |

| Cogent Tours | 8 |

| Cogent Velizy | 8 |

| nLighten Strasbourg SXB1 | 7 |

| UltraEdge Rennes | 7 |

| Equinix BX1 - Bordeaux | 7 |

| moji1 | 7 |

| Cogent Nice | 7 |

| Equinix PA1 - Paris, Roissy | 7 |

| ETIX Nantes #3 | 7 |

| Cogent Lille | 7 |

| TDF Datacenter Bordeaux Bouliac | 7 |

| Dyjix | 6 |

| nLighten Paris PAR2 | 6 |

| Digital Realty Paris PAR8 | 6 |

| OPCORE - DC5 / PAR5 | 6 |

| TDF Datacenter Aix Marseille | 6 |

| Datacenter Cyrès | 6 |

| Green Data - Nanterre | 6 |

| ETIX Paris #3 | 6 |

| Cogent Antibes | 5 |

| ETIX Paris #1 | 5 |

| Neuf Cesson | 5 |

| Axione Lotim Telecom | 5 |

| Digital Realty Paris PAR4 | 5 |

| Axione ADTIM | 5 |

| UltraEdge Rezé | 5 |

| Maxnod | 4 |

| UltraEdge Toulouse | 4 |

| Orange / Val de Rueil | 4 |

| Hotel des Telecoms | 4 |

| UltraEdge Montpellier | 4 |

| TDF Datacenter Lille Lambersart | 4 |

| 10 Rue des Frères Peuge | 3 |

| Salamandre | 3 |

| MCI/Verizon Paris St Denis | 3 |

| Prosoluce SG-1 Datacenter | 3 |

| Advanced MedioMatrix | 3 |

| Hexanet - DC Sabine | 3 |

| Montpellier Internet Telecom Datacenter | 3 |

| LASOTEL PIXEL | 3 |

| EXA Edge DC Nice | 3 |

| UltraEdge Grenoble | 3 |

| Comarch France #1 | 3 |

| COLT DC Paris II | 3 |

| APPLIWAVE - CBO | 3 |

| ITinSell Cloud Datacenter | 3 |

| Haute-Saône Numérique | 3 |

| Axione Limousin | 3 |

| Hexanet - DC Roland | 3 |

| Aqua Ray Aurora | 3 |

| D-LAKE | 3 |

| UltraEdge Lille | 2 |

| Ecocenter | 2 |

| dc2scale PAR4x (Meudon) | 2 |

| Somme-numerique DC1 | 2 |

| XL360 | 2 |

| Completel Val de Reuil | 2 |

| Cassin1 | 2 |

| Ad Valem Technologies - France (Saint-Denis) | 2 |

| DTIX Dijon | 2 |

| TDF Datacenter Paris Fort de Romainville | 2 |

| Celeste Marilyn | 2 |

| PoP Faraday (Rouen) | 2 |

| Techcrea Valenciennes | 2 |

| TAS Sophia | 2 |

| XSALTO Grenoble | 2 |

| dc2scale PAR5 (Vélizy-Villacoublay) | 2 |

| DATAGREX | 2 |

| DATA4 Paris Marcoussis PAR2 | 2 |

| Cogent Paris | 2 |

| NeoCenter Paris | 2 |

| nLighten Paris PAR1 | 2 |

| AtlasEdge DC Paris CDG001 | 2 |

| SI Cloud Montpellier | 2 |

| EXA Edge DC Bordeaux | 2 |

| System-Net HDC 1 | 2 |

| ETIX Vendée #1 | 2 |

| Groupe Cyllene - DC - Nanterre | 1 |

| Alpes Networks DataCenter | 1 |

| MEDIACTIVE MN3 | 1 |

| Eurofiber DC - AUC00 | 1 |

| RTDC | 1 |

| dc2scale ALP1 (Grenoble) | 1 |

| Orange / Chartres | 1 |

| EXA Edge DC Poitiers | 1 |

| Viatel Amiens | 1 |

| Extendo Datacenter Belfort | 1 |

| Hexatom Sophia Antipolis | 1 |

| Celeste Fil d’Ariane | 1 |

| IzarHost | 1 |

| NetaPOP Pontarlier | 1 |

| Ikoula IKDC2 | 1 |

| Groupe Cyllene - DC - Montigny les Bretonneux | 1 |

| Digital Realty Paris PAR12 | 1 |

| Fiducial Cloud LYO1 | 1 |

| NETICENTER | 1 |

| COLT DC Paris SouthWest | 1 |

| OT - Capella | 1 |

| EXA Edge DC Marseille | 1 |

| OT - Armor | 1 |

| NetaPOP Besançon | 1 |

| Multicoms Paris (Velizy) | 1 |

| COLT DC Paris III | 1 |

| BT-BLUE Datacenter 1 | 1 |

| Dataxion France DTX01 | 1 |

| OPCORE - DC4 / PAR4 | 1 |

| Castle-IT Tours | 1 |

| Neuf Rouen | 1 |

| Neuf Reims | 1 |

| Thésée Datacenter | 1 |

| Sanef Telecom Reims | 1 |

| Ultraedge Canteleu | 1 |

| Groupe Cyllene - DC - Courbevoie | 1 |

| BB1 | 0 |

| ICODIA NETWORK INTEGRITY | 0 |

| UltraEdge Velizy | 0 |

| Cloudata | 0 |

| MENGINE | 0 |

| Centrinuity Toulouse | 0 |

| EXA Edge DC Strasbourg | 0 |

| HELIANTIS | 0 |

| Alionis VBO | 0 |

| DTiX Chalon-sur-Saône | 0 |

| Alliance Réseaux | 0 |

| nLighten Sophia Antipolis NCE2 | 0 |

| Magic OnLine | 0 |

| RUBIX DATACENTER - DC-1 | 0 |

| VirtuaCenter Auxerre | 0 |

| Serinya Telecom | 0 |

| EXA Edge DC Vauchelles | 0 |

| dc2scale Nanterre | 0 |

| nLighten Paris PAR3 | 0 |

| REDHEBERG SAS | 0 |

| Metroptics Datacenter | 0 |

| connect-ix | 0 |

| Ouiherberg Aimargues | 0 |

| EXA Edge DC Nancy | 0 |

| EXA Edge DC Ychoux | 0 |

| Civicos Networking DCROUBAIX | 0 |

| Betech Solution | 0 |

| Crypteo Marssac | 0 |

| dc2scale LIL1 (Lille Datacenter) | 0 |

| EXA Edge DC Sequedin | 0 |

| dc2scale MRS1 (Marseille datacenter) | 0 |

| Reliance Plerin | 0 |

| PHOCEA DC-M1 | 0 |

| Neuf Caen | 0 |

| Smartdc Paris | 0 |

| Digital Realty Paris PAR13 | 0 |

| ATE #1 | 0 |

| SynAApS | 0 |

| DARVA Hosting | 0 |

| PAM00 | 0 |

| Sigma DC3 | 0 |

| OT - Rezé | 0 |

| Reliance St. Denis | 0 |

| Association Alsace Reseau Neutre | 0 |

| EXA Edge DC Toulouse | 0 |

| IMADIFF | 0 |

| Sipartech Paris | 0 |

| ADISTA Groupe | 0 |

| EXA Edge DC Willerval | 0 |

| Firstheberg | 0 |


**Summary:** 225 data center facilities identified in FR.

**Interpretation:**

Facilities with high AS colocation counts are the most critical nodes in the country's enabling infrastructure. Geographic concentration of these hubs in a single city or operator represents a resilience risk. A healthy ecosystem has multiple well-distributed facilities with significant colocation.

**Query 2 — Data center operators (concentration risk)**

```cypher
// For each data center in the country, lists the operator (organization) that manages it.
// Helps assess whether the data center market is dominated by one or a few operators (concentration risk).
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (f:Facility)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (f)-[:MANAGED_BY]->(org:Organization)
RETURN org.name AS Operator, COUNT(DISTINCT f) AS DataCenterCount
ORDER BY DataCenterCount DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Data Center Operator Concentration in FR

This analysis identifies the organizations managing data center facilities in the country and counts how many facilities each operator controls. Heavy concentration in one or two operators indicates a structural resilience risk.


**Operators by Number of Facilities Managed:**

| Operator | Facilities Managed |
|----------|--------------------|

| Cogent Communications, Inc. | 16 |

| UltraEdge | 12 |

| Etix Everywhere | 12 |

| Digital Realty | 11 |

| EXA Infrastructure | 11 |

| Equinix, Inc. | 9 |

| nLighten HQ BV | 8 |

| dc2scale SAS | 8 |

| TDF | 5 |

| Eurofiber France | 5 |

| Colt Technology Services Group | 4 |

| OPCORE | 4 |

| Neuf Cegetel SA. | 4 |

| Groupe Oceanet Technology | 4 |

| Telehouse - Global Data Centers | 3 |

| Cyllene SAS | 3 |

| Free Pro | 3 |

| Sipartech SAS | 2 |

| Zayo Group | 2 |

| DTiX SAS | 2 |

| DATA4 s.a r.l | 2 |

| Hexanet SAS | 2 |

| Celeste SAS | 2 |

| Netalis SAS | 2 |

| Ikoula Net SAS | 2 |

| WEBINDUSTRIE | 2 |

| FLAG Telecom | 2 |

| Alpes Networks SAS | 1 |

| MEDIACTIVE GROUP | 1 |

| ICODIA | 1 |

| ABICOM SAS | 1 |

| Adeli | 1 |

| ResoLv SARL | 1 |

| Cloudata | 1 |

| IELO-LIAZO SERVICES SAS | 1 |

| Penta C.V. | 1 |

| Orange S.A. | 1 |

| MENGINE | 1 |

| Centrinuity Toulouse | 1 |

| Verizon Communications, Inc. | 1 |

| HELIANTIS SAS | 1 |

| Alionis | 1 |

| PROSOLUCE SAS | 1 |

| Global Switch | 1 |

| ★ Dyjix SAS | 1 |

| Alliance Reseaux SAS | 1 |

| Treefaz | 1 |

| Somme-numerique DC1 | 1 |

| Orange / Val de Rueil | 1 |

| Magic OnLine | 1 |

| Xavier Lafaure | 1 |

| Completel SAS | 1 |

| Datacampus SAS | 1 |

| RUBIX DATACENTER | 1 |

| Ad Valem Technologies | 1 |

| Viatel Amiens | 1 |

| Advanced MedioMatrix | 1 |

| Virtua Networks | 1 |

| Extendo Datacenter | 1 |

| Serinya Telecom | 1 |

| Hexatom S.A.R.L. | 1 |

| Orange Business - La Fabrique | 1 |

| IZARLINK SAS | 1 |

| moji | 1 |

| Quantic Telecom SAS | 1 |

| Techcrea | 1 |

| Montpellier Internet Telecom Datacenter | 1 |

| TelcoCenter | 1 |

| LASOTEL SAS | 1 |

| TAS France | 1 |

| XSALTO | 1 |

| NEXEREN | 1 |

| REDHEBERG SAS | 1 |

| Metroptics | 1 |

| SAS CONNECT-IX | 1 |

| OuiHeberg SARL | 1 |

| Fiducial Cloud Organisation | 1 |

| Axione Lotim Telecom | 1 |

| Civicos Networking, S.L.U. | 1 |

| DATAGREX SAS | 1 |

| BeTech Solution | 1 |

| AZA TELECOM SARL | 1 |

| GREEN DATA SAS | 1 |

| Comarch SAS | 1 |

| PHOCEA DC | 1 |

| Axione Adtim | 1 |

| Smartdc | 1 |

| AtlasEdge | 1 |

| ATE - Avenir Télématique | 1 |

| MULTICOMS FACILITIES MANAGEMENT | 1 |

| Centre de Calcul de l'Institut National de Physique NuclÃ©aire et de Physique des Particules | 1 |

| Bretagne Telecom | 1 |

| SynAAps | 1 |

| DEVELOPPEMENT D'APPLICATIONS SUR RESEAUX A VALEUR AJOUTEE SA | 1 |

| ITinSell Cloud | 1 |

| SI Cloud SASU | 1 |

| EQUADEX SAS | 1 |

| SIGMA INFORMATIQUE SAS | 1 |

| Département de la Haute-Saône | 1 |

| EASYTEAM (ex DATAXION) | 1 |

| Caste-IT SAS | 1 |

| Association Alsace Reseau Neutre | 1 |

| Axione Limousin | 1 |

| System-Net SAS | 1 |

| IMA'DIFF | 1 |

| Aqua Ray | 1 |

| Thésée Datacenter | 1 |

| Sanef Telecom | 1 |

| Firstheberg | 1 |

| D-LAKE SAS | 1 |


**Interpretation:**

A data center market dominated by one or two large operators creates systemic risk — a business failure, regulatory action, or outage affecting that operator can impact a disproportionate share of the country's internet infrastructure. Diversity of operators is a positive resilience indicator.

**Query 3 — Significant ASes not colocated in any data center**

```cypher
// Identifies the most significant ASes in the country that are not colocated in any
// data center facility. Ranked by prefix count (routing footprint) so the most
// infrastructure-relevant networks appear first.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
WHERE NOT (a)-[:LOCATED_IN]->(:Facility)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)
WITH a, MIN(n.name) AS NetworkName, COUNT(DISTINCT pfx) AS PrefixCount
RETURN DISTINCT a.asn AS ASN, NetworkName, PrefixCount
ORDER BY PrefixCount DESC
LIMIT 20;
```

> **Output:** 

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Significant Networks Without Data Center Presence in FR

This analysis identifies the most significant Autonomous Systems in the country (ranked by routing footprint / prefix count) that are not colocated in any physical data center facility known to IYP/PeeringDB. These are networks with real infrastructure weight but no recorded physical colocation presence.


**Top ASes With No Known Colocation (by Prefix Count):**

| ASN | Network Name | Prefixes Announced |
|-----|--------------|--------------------|

| AS29066 | VELIANET-AS | 435 |

| AS62610 | ZEN-DPS | 288 |

| AS8677 | WORLDLINE | 200 |

| AS12696 | AXA Technology Services France GIE | 115 |

| AS2060 | FR-RENATER | 91 |

| AS207147 | NETCOM-AS | 82 |

| AS34949 | IDLINE SAS | 69 |

| AS60855 | DISIC-RIE-AS | 65 |

| AS210403 | Groupe LWS SARL | 56 |

| AS25215 | BNP PARIBAS S.A. | 55 |

| AS206178 | AWEBO | 50 |

| AS205710 | Association CREALAB | 50 |

| AS200546 | ALEXANDRE-SAGE-TRADING-AS-VELYS-SOFTWARE Alexandre SAGE trading as VELYS SOFTWARE | 50 |

| AS206445 | LE RESEAU VERT | 50 |

| AS207480 | ALGOMEDIA | 50 |

| AS211980 | Association ECHOES | 50 |

| AS207001 | Association LOS AMIGOS | 50 |

| AS206809 | PRO RESEAU | 48 |

| AS206778 | OPTA | 48 |

| AS215727 | ASNSWORLDWIDE | 47 |


**Interpretation:**

Networks with high prefix counts that lack colocation data represent a gap in infrastructure visibility. They may be operating from on-premise facilities, have incomplete PeeringDB records, or be deliberately absent from public colocation registries. Large ASes not present in any data center are more exposed to single-point-of-failure outages and reduce the country's overall infrastructure resilience.



### 1.1.2 IXP Coverage

**Query 1 — IXPs and their hosting facilities**

```cypher
// Lists all Internet Exchange Points (IXPs) located in a country,
// along with the data center facilities where each IXP is hosted.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (i)-[:LOCATED_IN]->(f:Facility)
RETURN i.name AS IXP, COLLECT(DISTINCT f.name) AS Facilities
ORDER BY SIZE(Facilities) DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: IXP Coverage and Facility Distribution in FR

This analysis maps the Internet Exchange Points (IXPs) present in the country and the physical data center facilities where they are hosted. IXP coverage is a direct measure of how well the country's network infrastructure enables efficient, local traffic exchange — reducing latency and transit costs.


**IXP Facility Distribution:**

| IXP Name | Hosting Facilities |
|----------|--------------------|

| nine | Seeweb Milano Caldera, Digital Realty Marseille MRS1/2/3/4, nLighten Lyon LYS1, Equinix PA2 - Paris, Saint-Denis, ETIX Montpellier #1, UltraEdge Bordeaux, Telehouse - London (Docklands West), ETIX Lille #2, Telehouse - Paris 2 (Voltaire - Léon Frot), UltraEdge Lyon-Venissieux, Equinix AM7 - Amsterdam, Kuiperberweg, Equinix ZH4 - Zurich, ETIX Lille #1, Equinix FR5 - Frankfurt, KleyerStrasse, Free Pro - Marseille - MRS1, OPCORE - DC3 / PAR3, moji1, NIKHEF Amsterdam |

| Hopus | Digital Realty Frankfurt FRA1-16, OPCORE - DC2 / PAR2, OPCORE - DC3 / PAR3, Telehouse - Paris 1 (Jeûneurs), Equinix GV1 - Geneva, City, UltraEdge Paris - Courbevoie, Equinix ZH2 - Zurich, Equinix PA2 - Paris, Saint-Denis, colozueri.ch Zurich, Digital Realty Marseille MRS1/2/3/4, Equinix PA3 - Paris, Saint-Denis, Telehouse - Paris 2 (Voltaire - Léon Frot), NIKHEF Amsterdam, UltraEdge Lyon-Venissieux |

| France-IX Paris | Telehouse - Paris 2 (Voltaire - Léon Frot), Digital Realty Paris PAR5, Equinix PA6 - Paris, Condorcet, OPCORE - DC3 / PAR3, Digital Realty Paris PAR2, OPCORE - DC2 / PAR2, Telehouse - Paris 3 (Magny), Equinix PA7 - Paris, Energy Park, DATA4 Paris Marcoussis - PAR1 |

| Equinix Paris | Equinix PA4 - Paris, Pantin, Telehouse - Paris 2 (Voltaire - Léon Frot), Equinix PA3 - Paris, Saint-Denis, Equinix PA2 - Paris, Saint-Denis, Equinix PA7 - Paris, Energy Park, Equinix PA5 - Paris, Victor Hugo, Equinix PA6 - Paris, Condorcet, Equinix PA10 - Paris, Saint-Denis |

| France-IX AURA | ETIX Lyon #1, UltraEdge Lyon-Venissieux, Free Pro - Limonest, Cogent Grenoble, Orange Business - La Fabrique [Grenoble], CC IN2P3 |

| SBG-IX | nLighten Strasbourg SXB1, Cogent Strasbourg, UltraEdge Strasbourg |

| Lillix | ETIX Lille #1, ETIX Lille #3, ETIX Lille #2 |

| EuroRhine-IX | nLighten Strasbourg SXB1, Cogent Strasbourg, UltraEdge Strasbourg |

| Ouest.Network | Cogent Nantes, ETIX Nantes #1 |

| France-IX Marseille | Digital Realty Marseille MRS1/2/3/4, Free Pro - Marseille - MRS1 |

| SFINX | Telehouse - Paris 2 (Voltaire - Léon Frot), Digital Realty Paris PAR1 |

| MPLIX | Cogent Montpellier, ETIX Montpellier #1 |

| DE-CIX Marseille | Digital Realty Marseille MRS1/2/3/4, Free Pro - Marseille - MRS1 |

| BreizhIX | Cogent Rennes, TDF Datacenter Rennes Cesson |

| ERA-IX Paris | Telehouse - Paris 2 (Voltaire - Léon Frot) |

| Association HwHost | Digital Realty Paris PAR5 |

| France-IX Lille | ETIX Lille #2 |

| France-IX Bordeaux | Equinix BX1 - Bordeaux |

| France-IX Toulouse | Eurofiber DC - TLS00 |

| AuvernIX | (no facility data) |

| NormandIX | (no facility data) |

| BrestIX | (no facility data) |

| BéarnIX | (no facility data) |

| BGP.Exchange - Paris | (no facility data) |

| BGP.Exchange - Lyon | (no facility data) |


**Interpretation:**

IXPs present in more physical facilities are more resilient and accessible to a wider range of network operators. A country with multiple IXPs each hosted across diverse facilities has significantly better enabling infrastructure than one relying on a single facility or a single IXP.


**Query 2 — Local vs. foreign AS members per IXP**

```cypher
// Counts the local and international AS members for each IXP located in a country.
// Local = AS also registered in the same country. Foreign = AS from another country.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(ic:Country {country_code: $countryCode})
MATCH (i)<-[:MEMBER_OF]-(a:AS)
OPTIONAL MATCH (a)-[:COUNTRY]->(ac:Country)
WITH i, a, COLLECT(DISTINCT ac.country_code) AS member_countries
WITH i,
     COUNT(DISTINCT CASE WHEN $countryCode IN member_countries THEN a END) AS LocalMembers,
     COUNT(DISTINCT CASE WHEN NOT $countryCode IN member_countries THEN a END) AS ForeignMembers
RETURN i.name AS IXP, LocalMembers, ForeignMembers
ORDER BY LocalMembers DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Local vs. Foreign Membership at IXPs in FR

This analysis compares the number of local (domestic) versus foreign (international) Autonomous System members at each IXP in the country. IXPs that attract international networks indicate that the country is a significant regional peering hub, while purely domestic IXPs serve local traffic exchange.


**IXP Membership Breakdown:**

| IXP Name | Local Members | Foreign Members |
|----------|---------------|-----------------|

| France-IX Paris | 235 | 212 |

| Equinix Paris | 151 | 92 |

| France-IX AURA | 59 | 15 |

| nine | 48 | 31 |

| France-IX Marseille | 37 | 75 |

| Lillix | 32 | 8 |

| Hopus | 27 | 6 |

| SFINX | 19 | 5 |

| BreizhIX | 18 | 2 |

| AuvernIX | 12 | 1 |

| EuroRhine-IX | 10 | 1 |

| DE-CIX Marseille | 10 | 112 |

| France-IX Lille | 10 | 6 |

| BGP.Exchange - Paris | 10 | 34 |

| Ouest.Network | 9 | 0 |

| France-IX Toulouse | 9 | 4 |

| BéarnIX | 8 | 1 |

| BGP.Exchange - Lyon | 8 | 16 |

| SBG-IX | 3 | 2 |

| BrestIX | 2 | 0 |

| MPLIX | 2 | 0 |

| NormandIX | 1 | 0 |

| France-IX Bordeaux | 1 | 1 |


**Interpretation:**

A healthy IXP ecosystem has a mix of local members (showing domestic traffic stays local) and foreign members (showing the country is a regional internet hub). IXPs with very few local members relative to foreign members may indicate that local ISPs are not fully leveraging the local peering infrastructure.

**Query 3 — Top foreign networks at local IXPs (regional peering hub indicator)**

```cypher
// Finds the top foreign networks (by CAIDA ASRank) that are members of IXPs
// located in the country. Shows their global importance rank and which local
// IXPs they participate in. Indicates whether the country is a regional peering hub.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(ic:Country {country_code: $countryCode})
MATCH (i)<-[:MEMBER_OF]-(a:AS)
OPTIONAL MATCH (a)-[:COUNTRY]->(ac:Country)
WITH i, a, COLLECT(DISTINCT ac.country_code) AS member_countries
WHERE NOT $countryCode IN member_countries
OPTIONAL MATCH (a)-[rel:RANK]->(r:Ranking {name: 'CAIDA ASRank'})
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a.asn AS ASN, MIN(n.name) AS NetworkName, COLLECT(DISTINCT i.name) AS IXPs, MIN(rel.rank) AS CaidaRank
WHERE CaidaRank IS NOT NULL
RETURN ASN, NetworkName, IXPs, CaidaRank
ORDER BY CaidaRank ASC
LIMIT 15;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: International Networks at FR IXPs

This analysis identifies the highest-ranked international Autonomous Systems that are members of the country's IXPs, ranked by their CAIDA global AS rank (lower = more important). The presence of major global carriers and content networks at local IXPs is a strong indicator that the country is a recognized regional internet hub.


**Top International Networks Present:**

| ASN | Network Name | CAIDA Global Rank | IXPs Present At |
|-----|--------------|-------------------|-----------------|

| AS6939 | HURRICANE | #7 | Equinix Paris, France-IX Marseille, nine, DE-CIX Marseille, France-IX AURA, France-IX Paris |

| AS6461 | ZAYO-6461 | #8 | Equinix Paris, Lillix, France-IX Marseille, nine, France-IX AURA, France-IX Paris |

| AS9002 | RETN | #11 | France-IX Paris |

| AS12956 | TELXIUS | #13 | DE-CIX Marseille |

| AS1273 | CW | #14 | Equinix Paris |

| AS4637 | ASN-TELSTRA-GLOBAL | #16 | France-IX Paris |

| AS37468 | ANGOLA-CABLES | #21 | France-IX Marseille |

| AS9498 | BBIL-AP | #22 | DE-CIX Marseille |

| AS58453 | CMI-INT-HK | #26 | Equinix Paris, France-IX Paris |

| AS20485 | TRANSTELECOM | #27 | France-IX Paris |

| AS31133 | MF-MGSM-AS | #28 | DE-CIX Marseille |

| AS20764 | CJSC RASCOM | #29 | France-IX Paris |

| AS33891 | CORE-BACKBONE | #37 | France-IX Paris |

| AS15412 | FLAG Telecom | #43 | Equinix Paris, France-IX Marseille, France-IX Paris |

| AS8220 | COLT | #44 | Equinix Paris, France-IX Marseille, France-IX Paris |


**Interpretation:**

International tier-1 and major content networks appearing at local IXPs confirms that the country has sufficient market size and connectivity to attract global players. This drives down latency for local users and validates the country's strategic position in regional internet topology. Networks with a CAIDA rank below 100 are considered globally significant.

## 1.2 Fiber Ecosystem

### 1.2.1 Fiber 10km Reach

**Query 1 — Geographic coverage points of active operators**

```cypher
// Fiber reach approximation: counts geographic coverage points of ASes that
// actively originate BGP prefixes (i.e., are operating networks, not dormant registrations).
// More geographic points across more active operators = broader physical infrastructure reach.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)
WHERE (a)-[:ORIGINATE]->(:BGPPrefix)
OPTIONAL MATCH (a)-[:LOCATED_IN]->(p:Point)
RETURN c.name AS Country,
       count(DISTINCT p) AS GeoCoveragePoints,
       count(DISTINCT a) AS ActiveOperators
ORDER BY GeoCoveragePoints DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Fiber Infrastructure Geographic Reach in FR

This analysis approximates the physical fiber reach of internet infrastructure by counting the number of distinct geographic Points associated with active Autonomous Systems (operators that actually announce BGP routes). More geographic points spread across more operators indicates a broader physical network footprint and suggests wider fiber deployment reach.


**Analysis Results:**

- Country: **France**
- Geographic coverage points: **1016**
- Active network operators: **1524**

**Interpretation:**

**1016** distinct geographic locations are registered by **1524** active network operators. A higher count indicates operators have declared infrastructure presence in more locations, which is a structural proxy for fiber or fixed network deployment breadth.


**Query 2 — Top operators by BGP prefix count and colocation footprint**

```cypher
// Top network operators by BGP prefix count and colocation footprint.
// Combines prefix count (routing footprint) with facility count (physical presence)
// to identify operators with the broadest infrastructure reach.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
OPTIONAL MATCH (a)-[:LOCATED_IN]->(f:Facility)-[:COUNTRY]->(c)
WITH a.asn AS ASN, MIN(n.name) AS OperatorName,
     COUNT(DISTINCT p) AS AnnouncedPrefixes,
     COUNT(DISTINCT f) AS FacilityPresence
RETURN ASN, OperatorName, AnnouncedPrefixes, FacilityPresence
ORDER BY AnnouncedPrefixes DESC
LIMIT 20;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Network Operators by Routing Footprint and Physical Presence in FR

This analysis ranks the country's active network operators by the number of BGP prefixes they announce (routing footprint) combined with the number of data center facilities they are present in (physical footprint). Operators with both high prefix counts and broad facility presence have the deepest infrastructure reach.


**Top Operators by Routing and Physical Footprint:**

| ASN | Operator Name | BGP Prefixes | Facilities |
|-----|---------------|--------------|------------|

| AS12322 | Free FR | 1065 | 14 |

| AS3215 | AS3215 | 984 | 6 |

| AS16276 | OVH | 792 | 5 |

| AS5511 | OPENTRANSIT | 576 | 21 |

| AS51167 | CONTABO | 570 | 0 |

| AS29066 | VELIANET-AS | 435 | 0 |

| AS2200 | FR-RENATER | 356 | 4 |

| AS63023 | AS-GLOBALTELEHOST | 323 | 2 |

| AS62610 | ZEN-DPS | 288 | 0 |

| AS46475 | LIMESTONENETWORKS | 262 | 1 |

| AS25369 | BANDWIDTH-AS | 207 | 1 |

| AS8677 | WORLDLINE | 200 | 0 |

| AS16347 | ADISTA SAS | 165 | 21 |

| AS15557 | LDCOMNET | 158 | 6 |

| AS1299 | Arelion | 139 | 14 |

| AS43350 | NFORCE | 130 | 0 |

| AS12696 | AXA Technology Services France GIE | 115 | 0 |

| AS34177 | CELESTE | 101 | 33 |

| AS2060 | FR-RENATER | 91 | 0 |

| AS25540 | ALPHALINK-AS | 91 | 5 |


**Interpretation:**

Operators with many BGP prefixes but low facility presence may be using third-party infrastructure. Operators with both high prefix counts and multiple facilities have the strongest physical infrastructure footprint and are the backbone of the country's fiber ecosystem.


**Query 3 — Multi-facility operators (physically distributed infrastructure)**

```cypher
// Multi-facility operators — active ASes present in more than one data center facility.
// Operators with presence across multiple facilities have physically distributed
// infrastructure, the strongest indicator of real geographic network reach.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:LOCATED_IN]->(f:Facility)
WHERE (a)-[:ORIGINATE]->(:BGPPrefix)
AND (f)-[:COUNTRY]->(c)
WITH a, COUNT(DISTINCT f) AS FacilityCount
WHERE FacilityCount > 1
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
RETURN a.asn AS ASN,
       MIN(n.name) AS OperatorName,
       FacilityCount AS NumberOfFacilities
ORDER BY FacilityCount DESC
LIMIT 20;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Multi-Facility Network Operators in FR

This analysis identifies network operators colocated in more than one data center facility within the country. An operator present across multiple facilities has physically distributed infrastructure — the strongest structural indicator of real geographic network reach and fiber deployment beyond a single site.


**Multi-Facility Operators:**

| ASN | Operator Name | Facilities |
|-----|---------------|------------|

| AS29075 | IELO | 68 |

| AS35625 | EUROFIBER-FRANCE | 52 |

| AS30781 | Free Pro | 42 |

| AS8309 | SIPARTECH | 41 |

| AS8218 | NEO-ASN | 34 |

| AS34177 | CELESTE | 33 |

| AS200780 | APPLIWAVE | 27 |

| AS39180 | LASOTEL | 25 |

| AS8487 | PHIBEE | 23 |

| AS62000 | NETRIX-AS | 23 |

| AS206120 | KOESIO Networks SAS | 22 |

| AS212815 | AS-DYJIX | 22 |

| AS16347 | ADISTA SAS | 21 |

| AS5511 | OPENTRANSIT | 21 |

| AS43646 | TDF | 20 |

| AS30889 | ADISTA SAS | 20 |

| AS34019 | HIVANE | 18 |

| AS47160 | MOJI | 16 |

| AS20565 | NETALIS | 16 |

| AS44407 | ASN-LINKT | 15 |


**Interpretation:**

Countries where many operators are present in multiple facilities have a more resilient, geographically dispersed fiber ecosystem. Operators appearing in only a single facility represent single-point-of-failure risks.


## 1.3 Mobile Connectivity

### 1.3.1 Network Coverage

**Query 1 — Network operator ecosystem overview (active vs. dormant ASes)**

```cypher
// Network operator ecosystem overview: counts active vs dormant ASes, facility
// presence, IXP membership, and geographic coverage for the country.
// Gives a single-glance health check of the network coverage ecosystem.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)
WITH c, a, COUNT(pfx) AS pfxCount
WITH c,
     COUNT(DISTINCT a) AS TotalASes,
     COUNT(DISTINCT CASE WHEN pfxCount > 0 THEN a END) AS ActiveASes,
     COUNT(DISTINCT CASE WHEN pfxCount = 0 THEN a END) AS DormantASes
RETURN c.name AS Country, TotalASes, ActiveASes, DormantASes,
       ROUND(ActiveASes * 100.0 / TotalASes * 100) / 100 AS ActivePercent;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Network Operator Ecosystem Health in FR

This analysis breaks down the country's Autonomous Systems into active operators (those announcing BGP routes) and dormant registrations (ASes with no active routing). The active-to-total ratio is a direct measure of ecosystem vitality — countries with many registered but inactive ASes have underutilized network capacity.


**Operator Ecosystem Overview:**

- Country: **France**
- Total Registered ASes: **2238**
- Active Operators (BGP): **1524** (68.1%)
- Dormant Registrations: **714**

**Interpretation:**

**1524** out of **2238** registered ASes are actively originating BGP routes (68.1%). A higher active percentage indicates a healthier, more competitive network ecosystem. Dormant ASes may represent unused allocations, acquired-but-undeployed resources, or legacy registrations.


**Query 2 — Physical infrastructure footprint (domestic vs. international facilities)**

```cypher
// Physical infrastructure footprint: counts domestic vs international facilities
// where the country's ASes are colocated. Domestic facility count measures local
// infrastructure depth; international presence shows global connectivity reach.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:LOCATED_IN]->(f:Facility)
OPTIONAL MATCH (f)-[:COUNTRY]->(fc:Country)
WITH c, f, fc.country_code AS FacilityCountry
RETURN c.name AS Country,
       COUNT(DISTINCT CASE WHEN FacilityCountry = $countryCode THEN f END) AS DomesticFacilities,
       COUNT(DISTINCT CASE WHEN FacilityCountry <> $countryCode THEN f END) AS InternationalFacilities,
       COUNT(DISTINCT f) AS TotalFacilities;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Physical Infrastructure Footprint in FR

This analysis counts the physical data center facilities where the country's ASes are colocated, separating domestic facilities (within the country) from international ones (abroad). Domestic facility count measures local infrastructure depth; international presence shows global connectivity reach.


**Infrastructure Footprint:**

- Country: **France**
- Domestic Facilities: **168**
- International Facilities: **453**
- Total Facilities: **621**

**Interpretation:**

**168** facilities are located within the country, while **453** are abroad. A strong domestic facility base is essential for network resilience — it means local traffic can be served locally. International presence indicates operators are globally connected, but over-reliance on foreign infrastructure is a resilience risk.


**Query 3 — IXP connectivity gap analysis**

```cypher
// IXP connectivity gap analysis: counts active ASes that are members of a
// domestic IXP vs those that are not. A high proportion of ASes outside the
// local IXP ecosystem is a key resilience weakness — traffic must route
// internationally instead of being exchanged locally.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
WHERE (a)-[:ORIGINATE]->()
OPTIONAL MATCH (a)-[:MEMBER_OF]->(i:IXP)-[:COUNTRY]->(c)
WITH c, a, COUNT(DISTINCT i) AS LocalIXPCount
RETURN c.name AS Country,
       COUNT(DISTINCT CASE WHEN LocalIXPCount > 0 THEN a END) AS IXPConnected,
       COUNT(DISTINCT CASE WHEN LocalIXPCount = 0 THEN a END) AS NotIXPConnected,
       COUNT(DISTINCT a) AS TotalActive,
       ROUND(COUNT(DISTINCT CASE WHEN LocalIXPCount > 0 THEN a END) * 100.0 /
             COUNT(DISTINCT a) * 100) / 100 AS IXPAdoptionPercent;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: IXP Connectivity Gap Analysis in FR

This analysis identifies how many active network operators are members of at least one domestic IXP versus those with no local IXP presence. ASes not connected to any domestic IXP must route all traffic via upstream transit providers, increasing costs and latency while reducing resilience.


**IXP Connectivity Overview:**

- Country: **France**
- Active ASes connected to a domestic IXP: **346**
- Active ASes NOT connected to any domestic IXP: **1178**
- Total Active ASes: **1524**
- IXP Adoption Rate: **22.7%**

**Interpretation:**

Only **22.7%** of active ASes are members of a domestic IXP. The remaining **1178** operators must rely entirely on upstream transit for traffic exchange. Increasing IXP adoption is one of the most impactful policy actions for improving network coverage resilience — it enables local traffic to stay local.



**Query 4 — Peering density analysis (domestic vs. international)**

```cypher
// Peering density analysis: breaks down peering connections into domestic
// (both ASes in the same country) vs international. High domestic peering
// means local traffic stays local; low domestic peering means traffic
// must route internationally — a critical resilience weakness.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:PEERS_WITH]-(b:AS)
OPTIONAL MATCH (b)-[:COUNTRY]->(bc:Country)
WITH c, b, COLLECT(DISTINCT bc.country_code) AS PeerCountries
RETURN c.name AS Country,
       COUNT(DISTINCT CASE WHEN $countryCode IN PeerCountries THEN b END) AS DomesticPeers,
       COUNT(DISTINCT CASE WHEN NOT $countryCode IN PeerCountries THEN b END) AS InternationalPeers,
       COUNT(DISTINCT b) AS TotalPeers;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Network Peering Density in FR

This analysis breaks down the country's peering relationships into domestic (both ASes in the same country) and international. High domestic peering density means local traffic can be exchanged locally; low domestic peering means traffic must route internationally — a critical resilience weakness.


**Peering Density Overview:**

- Country: **France**
- Domestic Peers: **1271**
- International Peers: **10613**
- Total Peers: **11884**

**Interpretation:**

**1271** domestic peers versus **10613** international peers. A healthy peering ecosystem has strong domestic interconnection so that local traffic doesn't need to leave the country. The ratio of domestic to international peering is a key indicator of network self-sufficiency and resilience.



### 1.3.2 Spectrum Allocation

**Query 1 — BGP prefix count breakdown by address family (IPv4/IPv6)**

```cypher
// BGP prefix count breakdown by address family — measures IP address space utilization.
// IPv4 prefix count shows existing deployment scale; IPv6 prefix count shows
// forward-looking address space adoption and future network capacity planning.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(p:BGPPrefix)
RETURN c.name AS Country,
       count(DISTINCT p)                                                    AS Originated_Prefixes,
       count(DISTINCT CASE WHEN p.af = 4 THEN p ELSE null END)             AS IPv4_Prefixes,
       count(DISTINCT CASE WHEN p.af = 6 THEN p ELSE null END)             AS IPv6_Prefixes,
       count(DISTINCT as)                                                   AS ActiveOperators,
       round(100.0 * count(DISTINCT CASE WHEN p.af = 6 THEN p ELSE null END)
             / count(DISTINCT p), 2)                                        AS IPv6_SharePercent
ORDER BY Originated_Prefixes DESC;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: IP Address Space Utilization in FR

This analysis measures the total BGP prefix footprint of the country's network operators, broken down by address family (IPv4 vs IPv6). In the IYP graph, this serves as the best available proxy for network capacity and address space allocation — a structural correlate of spectrum/address utilization maturity.


**Analysis Results:**

- Country: **France**
- Total BGP prefixes originated: **15996**
- IPv4 prefixes: **13138**
- IPv6 prefixes: **2858**
- Active operators: **1524**
- IPv6 share of prefix table: **17.87%**

**Interpretation:**

A higher total prefix count indicates greater IP address space allocation and more granular network segmentation. An increasing IPv6 share reflects modernization of the address space — operators planning for long-term scalability beyond IPv4 exhaustion.

**Query 2 — Top operators by prefix count with IPv6 adoption flag**

```cypher
// Top network operators by BGP prefix count — largest IP address space holders,
// broken down by IPv4/IPv6 with adoption readiness flag.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a, MIN(n.name) AS OperatorName,
     COUNT(DISTINCT CASE WHEN p.af = 4 THEN p END) AS IPv4Prefixes,
     COUNT(DISTINCT CASE WHEN p.af = 6 THEN p END) AS IPv6Prefixes
WITH a.asn AS ASN, OperatorName, IPv4Prefixes, IPv6Prefixes,
     (IPv4Prefixes + IPv6Prefixes) AS TotalPrefixes,
     CASE WHEN IPv6Prefixes > 0 THEN 'Yes' ELSE 'No' END AS IPv6Adopted
RETURN ASN, OperatorName, TotalPrefixes, IPv4Prefixes, IPv6Prefixes, IPv6Adopted
ORDER BY TotalPrefixes DESC
LIMIT 20;
```

> **Output :**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Largest IP Address Space Holders in FR

This analysis identifies the top 20 network operators in the country by number of BGP prefixes announced, broken down by IPv4 and IPv6, with an IPv6 adoption flag. Operators with zero IPv6 prefixes are not future-ready and represent resilience risks as IPv4 address space becomes increasingly scarce.


**Top Operators by Address Space:**

| ASN | Operator Name | Total Prefixes | IPv4 | IPv6 | IPv6 Adopted |
|-----|---------------|----------------|------|------|--------------|

| AS12322 | Free FR | 1065 | 538 | 527 | Yes |

| AS3215 | AS3215 | 984 | 941 | 43 | Yes |

| AS16276 | OVH | 792 | 751 | 41 | Yes |

| AS5511 | OPENTRANSIT | 576 | 563 | 13 | Yes |

| AS51167 | CONTABO | 570 | 565 | 5 | Yes |

| AS29066 | VELIANET-AS | 435 | 425 | 10 | Yes |

| AS2200 | FR-RENATER | 356 | 354 | 2 | Yes |

| AS63023 | AS-GLOBALTELEHOST | 323 | 298 | 25 | Yes |

| AS62610 | ZEN-DPS | 288 | 209 | 79 | Yes |

| AS46475 | LIMESTONENETWORKS | 262 | 238 | 24 | Yes |

| AS25369 | BANDWIDTH-AS | 207 | 188 | 19 | Yes |

| AS8677 | WORLDLINE | 200 | 200 | 0 | No |

| AS16347 | ADISTA SAS | 165 | 147 | 18 | Yes |

| AS15557 | LDCOMNET | 158 | 146 | 12 | Yes |

| AS1299 | Arelion | 139 | 115 | 24 | Yes |

| AS43350 | NFORCE | 130 | 109 | 21 | Yes |

| AS12696 | AXA Technology Services France GIE | 115 | 115 | 0 | No |

| AS34177 | CELESTE | 101 | 90 | 11 | Yes |

| AS25540 | ALPHALINK-AS | 91 | 84 | 7 | Yes |

| AS2060 | FR-RENATER | 91 | 91 | 0 | No |


**Interpretation:**

Operators with large address space allocations are the backbone of the country's internet capacity. The IPv6 Adopted column highlights which major operators have modernized — those showing "No" are critical targets for IPv6 adoption programs, as IPv4 exhaustion threatens long-term scalability and resilience.


# 2. Market Readiness

## 2.1 Market Structure

### 2.1.1 Market Competition

**Query 1 — Market share per AS (population-weighted)**

```cypher
// Récupère la part de marché de chaque AS dans un pays donné.
// Le paramètre $countryCode doit être fourni lors de l'exécution (ex: 'CI' pour la Côte d'Ivoire).
MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)
// Récupère le nom de l'AS pour une meilleure lisibilité.
OPTIONAL MATCH (as)-[:NAME]->(n:Name)
WITH as, p, collect(DISTINCT n.name)[0] AS asName
RETURN as.asn AS asn,
       asName,
       p.percent AS marketSharePercent
ORDER BY marketSharePercent DESC
LIMIT 30;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Internet Market Share Distribution in FR

This analysis maps the market share of each Autonomous System (internet operator) in the country, measured by the percentage of the population they serve. This directly reflects the competitive landscape of the country's internet access market.


**Market Share by Operator (Top 30):**

| ASN | Operator Name | Market Share (%) |
|-----|---------------|------------------|

| AS3215 | AS3215 Orange S.A. | 35.38 |

| AS12322 | PROXAD Free SAS | 18.65 |

| AS5410 | BOUYGTEL-ISP Bouygues Telecom SA | 17.75 |

| AS15557 | LDCOMNET Societe Francaise Du Radiotelephone - SFR SA | 17.52 |

| AS51207 | FREEM Free Mobile SAS | 4.55 |

| AS16276 | OVH OVH SAS | 0.85 |

| AS63023 | AS-GLOBALTELEHOST - GTHost | 0.78 |

| AS12876 | AS12876 Scaleway SAS | 0.69 |

| AS51167 | CONTABO Contabo GmbH | 0.32 |

| AS31404 | Lycatel-AS LYCATEL DISTRIBUTION UK LIMITED | 0.26 |

| AS13335 | CLOUDFLARENET - Cloudflare, Inc. | 0.21 |

| AS30058 | FDCSERVERS - FDCservers.net | 0.21 |

| AS14593 | SPACEX-STARLINK - Space Exploration Technologies Corporation | 0.19 |

| AS21859 | ZEN-ECN | 0.17 |

| AS29066 | VELIANET-AS velia.net Internetdienste GmbH | 0.14 |

| AS16509 | AMAZON-02 - Amazon.com, Inc. | 0.14 |

| AS52075 | WIFIRST Wifirst S.A.S. | 0.12 |

| AS62610 | ZEN-DPS - Zenlayer Inc | 0.11 |

| AS212238 | CDNEXT Datacamp Limited | 0.09 |

| AS136787 | PACKETHUBSA-AS-AP PacketHub S.A. | 0.09 |

| AS2200 | FR-RENATER Reseau National de telecommunications pour la Technologie | 0.09 |

| AS199636 | FREEBOXPRO Free Pro SAS | 0.08 |

| AS42487 | Vialis-Moselle Vialis SEM | 0.08 |

| AS63949 | AKAMAI-LINODE-AP Akamai Connected Cloud | 0.08 |

| AS16347 | INHERENT ADISTA SAS | 0.07 |

| AS8362 | NordNet SA | 0.06 |

| AS41114 | ORNETHD ORNE THD SPL | 0.06 |

| AS8399 | SEWAN-FR SEWAN SAS | 0.05 |

| AS12727 | VIALIS Vialis SEM | 0.05 |

| AS174 | COGENT-174 - Cogent Communications, LLC | 0.05 |


**Interpretation:**

A market where the top operator holds more than 50% indicates a dominant-player market with limited competition. A healthy market has multiple operators each below 30% market share.


**Query 2 — Herfindahl-Hirschman Index (HHI) for market concentration**

```cypher
// Calculates the Herfindahl-Hirschman Index (HHI) for a country's internet market.
// HHI = sum of squared market shares. Higher HHI = more concentrated market.
// Thresholds: <1500 = Competitive, 1500-2500 = Moderately Concentrated, >2500 = Highly Concentrated.
// The parameter $countryCode must be provided during execution (e.g., 'CI', 'FR', 'KE').
MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)
WITH c, sum(p.percent^2) AS hhi, count(DISTINCT as) AS totalAS
RETURN hhi,
       totalAS,
       CASE
           WHEN hhi < 1500 THEN 'Competitive Market'
           WHEN hhi >= 1500 AND hhi <= 2500 THEN 'Moderately Concentrated Market'
           ELSE 'Highly Concentrated Market'
       END AS marketConcentration;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Internet Market Concentration (HHI) in FR

This analysis calculates the Herfindahl-Hirschman Index (HHI) — the standard economic measure of market concentration used by competition regulators worldwide. The HHI is the sum of the squares of each operator's market share. A higher HHI indicates a more concentrated, less competitive market.


**Market Concentration Results:**

- Total operators in market: **65**
- HHI Score: **2245**
- Market Assessment: **Moderately Concentrated Market**

**HHI Reference Scale:**

| HHI Range | Assessment |
|-----------|------------|
| < 1,500 | Competitive Market |
| 1,500 to 2,500 | Moderately Concentrated Market |
| > 2,500 | Highly Concentrated Market |


### 2.1.2 Upstream Provider Diversity

**Query 1 — International transit providers and their local customer count**

```cypher
// Identifie les fournisseurs de transit pour un pays donné et compte leurs clients locaux.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
// Utilise BGPKIT (r.rel=1) pour trouver les relations Provider-to-Customer.
MATCH (as)-[r:PEERS_WITH {rel: 1}]->(provider:AS)
// S'assure que le fournisseur n'est pas lui-même local (focus sur le transit international).
WHERE NOT (provider)-[:COUNTRY]->(c)
WITH provider, count(DISTINCT as) AS localCustomers
// Récupère le nom du fournisseur pour une meilleure lisibilité.
OPTIONAL MATCH (provider)-[:NAME]->(n:Name)
WITH provider, localCustomers, collect(DISTINCT n.name)[0] AS providerName
RETURN provider.asn AS providerASN,
       providerName,
       localCustomers
ORDER BY localCustomers DESC
LIMIT 10;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Upstream Transit Provider Landscape for FR

This analysis identifies international Autonomous Systems (AS) that provide internet transit to local networks within the country. It ranks them by the number of local "customer" networks they serve. A high concentration of local networks relying on a single external provider indicates a potential Single Point of Failure (SPOF).


**Top Transit Providers by Local Customer Count:**


- **Rank 1:** RIPE-NCC-RIS-AS Reseaux IP Europeens Network Coordination Centre (RIPE NCC) (AS12654)
  Local Customer Networks: **7**

- **Rank 2:** BSO IX Reach Ltd (AS4455)
  Local Customer Networks: **4**

- **Rank 3:** M247 M247 Europe SRL (AS9009)
  Local Customer Networks: **3**

- **Rank 4:** AlexHost ALEXHOST SRL (AS200019)
  Local Customer Networks: **3**

- **Rank 5:** NETSKOPE - Netskope Inc (AS55256)
  Local Customer Networks: **3**

- **Rank 6:** OUTREMER-AS Outremer Telecom SAS (AS20776)
  Local Customer Networks: **3**

- **Rank 7:** PARADOXNETWORKS-LIMITED ParadoxNetworks Limited (AS52025)
  Local Customer Networks: **3**

- **Rank 8:** IP-Max IP-Max SA (AS25091)
  Local Customer Networks: **3**

- **Rank 9:** ACCENTURE - Accenture LLP (AS3573)
  Local Customer Networks: **3**

- **Rank 10:** ZEN-ECN (AS21859)
  Local Customer Networks: **3**


**Query 2 — Transit dependency measurement (IHR hegemony metric)**

```cypher
// Mesure la dépendance moyenne des AS d'un pays envers leurs fournisseurs de transit.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
// Utilise la relation de dépendance et la métrique d'hégémonie de l'IHR.
MATCH (as)-[d:DEPENDS_ON]->(provider:AS)
// Filtre pour les dépendances significatives afin de réduire le bruit.
WHERE d.hege > 0.1 AND NOT (provider)-[:COUNTRY]->(c)
WITH provider, avg(d.hege) AS averageHegemony, count(DISTINCT as) AS dependentASNs
OPTIONAL MATCH (provider)-[:NAME]->(n:Name)
WITH provider, averageHegemony, dependentASNs, collect(DISTINCT n.name)[0] AS providerName
RETURN provider.asn AS providerASN,
       providerName,
       averageHegemony,
       dependentASNs
ORDER BY dependentASNs DESC, averageHegemony DESC
LIMIT 50;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Critical Upstream Dependency (Hegemony) for FR

While the previous analysis counted connections, this metric quantifies the *criticality* of those connections using the "Hegemony" score (0 to 1). A high hegemony score indicates that a provider is unavoidable for the networks that depend on it. High scores here suggest deep structural dependencies and significant resilience risks.


**1. Highest Risk (by Hegemony Score - "The Single Point of Failure"):**
Providers that have near-total control over the local networks they serve.



- **Rank 1:** AMAZON-02 - Amazon.com, Inc. (AS16509)
  Average Hegemony Score: **1.000**
  (Affecting 4 local networks)

- **Rank 2:** PROLEXIC-TECHNOLOGIES-DDOS-MITIGATION-NETWORK - Akamai Technologies, Inc. (AS32787)
  Average Hegemony Score: **0.903**
  (Affecting 12 local networks)

- **Rank 3:** VIRTUO - 12651980 CANADA INC. (AS399486)
  Average Hegemony Score: **0.851**
  (Affecting 15 local networks)

- **Rank 4:** CANALPLUSTELECOM Canal + Telecom SAS (AS21351)
  Average Hegemony Score: **0.836**
  (Affecting 9 local networks)

- **Rank 5:** ATGS-MMD-AS - AT&T Enterprises, LLC (AS2686)
  Average Hegemony Score: **0.829**
  (Affecting 4 local networks)

- **Rank 6:** LAGRANGE Lagrange Cloud Technologies Limited (AS209735)
  Average Hegemony Score: **0.813**
  (Affecting 13 local networks)

- **Rank 7:** UUNET - Verizon Business (AS702)
  Average Hegemony Score: **0.793**
  (Affecting 10 local networks)

- **Rank 8:** ROUTE64_ORG Johannes Ernst (AS212895)
  Average Hegemony Score: **0.791**
  (Affecting 10 local networks)

- **Rank 9:** AS-VULTR - The Constant Company, LLC (AS20473)
  Average Hegemony Score: **0.780**
  (Affecting 25 local networks)

- **Rank 10:** STORMWALL-AS StormWall s.r.o. (AS59796)
  Average Hegemony Score: **0.772**
  (Affecting 3 local networks)


**2. Widest Impact (by Affected Networks - "The Widespread Risk"):**
Providers that provide internet to the largest sheer volume of local networks.



- **Rank 1:** HURRICANE - Hurricane Electric LLC (AS6939)
  Average Hegemony Score: **0.362**
  (Affecting 762 local networks)

- **Rank 2:** COGENT-174 - Cogent Communications, LLC (AS174)
  Average Hegemony Score: **0.460**
  (Affecting 410 local networks)

- **Rank 3:** LEVEL3 - Level 3 Parent, LLC (AS3356)
  Average Hegemony Score: **0.330**
  (Affecting 161 local networks)

- **Rank 4:** SEABONE-NET TELECOM ITALIA SPARKLE S.p.A. (AS6762)
  Average Hegemony Score: **0.284**
  (Affecting 131 local networks)

- **Rank 5:** ZAYO-6461 - Zayo Bandwidth (AS6461)
  Average Hegemony Score: **0.445**
  (Affecting 105 local networks)

- **Rank 6:** COLT COLT Technology Services Group Limited (AS8220)
  Average Hegemony Score: **0.686**
  (Affecting 99 local networks)

- **Rank 7:** GSLNETWORKS-AS-AP GSL Networks Pty LTD (AS137409)
  Average Hegemony Score: **0.344**
  (Affecting 91 local networks)

- **Rank 8:** GTT-BACKBONE GTT Communications Inc. (AS3257)
  Average Hegemony Score: **0.440**
  (Affecting 60 local networks)

- **Rank 9:** Infomaniak-AS Infomaniak Network SA (AS29222)
  Average Hegemony Score: **0.125**
  (Affecting 56 local networks)

- **Rank 10:** NTT-DATA-2914 - NTT America, Inc. (AS2914)
  Average Hegemony Score: **0.250**
  (Affecting 48 local networks)


## 2.2 Traffic Localization

### 2.2.1 Domain Count

**Query 1 — Most queried ccTLD domains from within the country**

```cypher
// Identifies the ccTLD domains most frequently queried from within the country.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})
// Filters domains that end with the country's ccTLD (e.g., .sn)
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Finds the query relationship from this country (source: Cloudflare Radar)
MATCH (d)-[q:QUERIED_FROM]->(c)
WHERE q.value IS NOT NULL

RETURN d.name AS localDomain,
       q.value AS percentageOfQueriesInCountry
ORDER BY percentageOfQueriesInCountry DESC
LIMIT 20;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Popularity of Local Domains (ccTLD) in FR

This analysis verifies if locally registered domains (e.g., .sn, .jp) are actually consumed by local users. It measures the percentage of DNS queries originating from the country that target these specific domains. High usage suggests a relevant local content ecosystem, whereas low usage implies users primarily consume foreign content.


**Most Queried Local Domains:**


- **Rank 1:** ameli.fr
  Share of Local Queries: **91.9732%**

- **Rank 2:** louvre.fr
  Share of Local Queries: **87.4046%**

- **Rank 3:** huffingtonpost.fr
  Share of Local Queries: **86.8132%**

- **Rank 4:** doctolib.fr
  Share of Local Queries: **82.9384%**

- **Rank 5:** leroymerlin.fr
  Share of Local Queries: **81.4268%**

- **Rank 6:** lepoint.fr
  Share of Local Queries: **76.4045%**

- **Rank 7:** leboncoin.fr
  Share of Local Queries: **75.0000%**

- **Rank 8:** impots.gouv.fr
  Share of Local Queries: **75.0000%**

- **Rank 9:** vinted.fr
  Share of Local Queries: **72.3491%**

- **Rank 10:** labanquepostale.fr
  Share of Local Queries: **70.7071%**

- **Rank 11:** cic.fr
  Share of Local Queries: **70.3704%**

- **Rank 12:** cnil.fr
  Share of Local Queries: **70.0000%**

- **Rank 13:** caf.fr
  Share of Local Queries: **69.0141%**

- **Rank 14:** sg.fr
  Share of Local Queries: **66.6667%**

- **Rank 15:** lemonde.fr
  Share of Local Queries: **66.0656%**

- **Rank 16:** tf1info.fr
  Share of Local Queries: **65.3061%**

- **Rank 17:** laredoute.fr
  Share of Local Queries: **64.4628%**

- **Rank 18:** rugbyrama.fr
  Share of Local Queries: **64.2857%**

- **Rank 19:** creditmutuel.fr
  Share of Local Queries: **63.8889%**

- **Rank 20:** lesechos.fr
  Share of Local Queries: **62.6667%**

**Query 2 — Geographic distribution of hosting for top ccTLD domains**

```cypher
// Analyses the geographic distribution of hosting for the top 100 ccTLD domains.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Focus on popular domains (source: Tranco) for a relevant analysis.
MATCH (d)-[r:RANK]->(:Ranking {name:"Tranco top 1M"})
WITH d ORDER BY r.rank LIMIT 100

// Expand search to include the domain itself, its subdomains, and its hostnames
OPTIONAL MATCH (d)-[:RESOLVES_TO]->(ip1:IP)
OPTIONAL MATCH (d)<-[:PARENT*1..2]-(sub:DomainName)-[:RESOLVES_TO]->(ip2:IP)
OPTIONAL MATCH (d)-[:MANAGED_BY]->(h:HostName)-[:RESOLVES_TO]->(ip3:IP)

WITH d, coalesce(ip1, ip2, ip3) AS ip
WHERE ip IS NOT NULL

// Trace hosting country via the confirmed IYP path
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)
MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

WITH hostingCountry, count(DISTINCT d) AS domainCount
RETURN hostingCountry.country_code AS hostingCountryCode,
       domainCount
ORDER BY domainCount DESC;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Hosting Locations of Top Local Domains for FR

This metric analyzes where the top 100 most popular local domains (ccTLD) are physically hosted.
- **Local Hosting:** Desirable for data sovereignty, lower latency, and reduced reliance on international transit.
- **Foreign Hosting:** Indicates "content leakage," where local traffic must traverse international links to access local content.


**Hosting Distribution (by Country):**


- **US**: 51 domain(s)
  
  *(Foreign Hosting)*
  

- **FR**: 49 domain(s)
  
  *(LOCAL HOSTING - Good for resilience)*
  

- **AU**: 21 domain(s)
  
  *(Foreign Hosting)*
  

- **AF**: 19 domain(s)
  
  *(Foreign Hosting)*
  

- **NL**: 13 domain(s)
  
  *(Foreign Hosting)*
  

- **GB**: 6 domain(s)
  
  *(Foreign Hosting)*
  

- **CH**: 4 domain(s)
  
  *(Foreign Hosting)*
  

- **AT**: 4 domain(s)
  
  *(Foreign Hosting)*
  

- **BG**: 3 domain(s)
  
  *(Foreign Hosting)*
  

- **BR**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **IT**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **TR**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **MX**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **CO**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **CL**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **LT**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **UY**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **HK**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **KH**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **AE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **PA**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **AR**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **UA**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **RU**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **MU**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **KE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **RO**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **BH**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **AO**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **RS**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **SE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **DE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **DK**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **PH**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **LV**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **ES**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **SG**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **VN**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **LK**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **AD**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **CD**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **BE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **ZA**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **AZ**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **LU**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **TH**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **EE**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **EU**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **CA**: 2 domain(s)
  
  *(Foreign Hosting)*
  

- **CZ**: 1 domain(s)
  
  *(Foreign Hosting)*

### 2.2.2 E-Gov Index Score

**Query 1 — Top local domains by query percentage**

```cypher
// Query 1: Top Local Domains
MATCH (c:Country {country_code: $countryCode})
MATCH (d:DomainName)-[q:QUERIED_FROM]->(c)
WHERE d.name ENDS WITH '.' + toLower($countryCode)
OPTIONAL MATCH (d)-[r:RANK]->(:Ranking {name:"Tranco top 1M"})
RETURN d.name AS domainName,
       q.value AS percentageOfLocalQueries,
       r.rank AS trancoRank
ORDER BY percentageOfLocalQueries DESC, trancoRank ASC
LIMIT 25;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Top Locally Accessed Domains (ccTLD) in FR

This analysis identifies the most frequently queried local domains (ending in .fr) from within the country. While not all are government sites, this list highlights the most critical digital services for the local population. Identifying these domains is the first step to analyzing the resilience of the national digital ecosystem.


**Most Popular Local Domains:**


- **Rank 1:** ameli.fr
  Local Query Share: **91.9732%**
  
  (Global Tranco Rank: 4954)
  

- **Rank 2:** louvre.fr
  Local Query Share: **87.4046%**
  
  (Global Tranco Rank: 6231)
  

- **Rank 3:** huffingtonpost.fr
  Local Query Share: **86.8132%**
  
  (Global Tranco Rank: 5614)
  

- **Rank 4:** doctolib.fr
  Local Query Share: **82.9384%**
  
  (Global Tranco Rank: 5094)
  

- **Rank 5:** leroymerlin.fr
  Local Query Share: **81.4268%**
  
  (Global Tranco Rank: 1287)
  

- **Rank 6:** lepoint.fr
  Local Query Share: **76.4045%**
  
  (Global Tranco Rank: 5703)
  

- **Rank 7:** leboncoin.fr
  Local Query Share: **75.0000%**
  
  (Global Tranco Rank: 1111)
  

- **Rank 8:** impots.gouv.fr
  Local Query Share: **75.0000%**
  
  (Global Tranco Rank: 8698)
  

- **Rank 9:** vinted.fr
  Local Query Share: **72.3491%**
  
  (Global Tranco Rank: 1857)
  

- **Rank 10:** labanquepostale.fr
  Local Query Share: **70.7071%**
  
  (Global Tranco Rank: 7772)
  

- **Rank 11:** cic.fr
  Local Query Share: **70.3704%**
  
  (Global Tranco Rank: 8550)
  

- **Rank 12:** cnil.fr
  Local Query Share: **70.0000%**
  
  (Global Tranco Rank: 3428)
  

- **Rank 13:** caf.fr
  Local Query Share: **69.0141%**
  
  (Global Tranco Rank: 6257)
  

- **Rank 14:** sg.fr
  Local Query Share: **66.6667%**
  
  (Global Tranco Rank: 7474)
  

- **Rank 15:** lemonde.fr
  Local Query Share: **66.0656%**
  
  (Global Tranco Rank: 693)
  

- **Rank 16:** tf1info.fr
  Local Query Share: **65.3061%**
  
  (Global Tranco Rank: 6164)
  

- **Rank 17:** laredoute.fr
  Local Query Share: **64.4628%**
  
  (Global Tranco Rank: 6867)
  

- **Rank 18:** rugbyrama.fr
  Local Query Share: **64.2857%**
  
  (Global Tranco Rank: 9150)
  

- **Rank 19:** creditmutuel.fr
  Local Query Share: **63.8889%**
  
  (Global Tranco Rank: 7616)
  

- **Rank 20:** lesechos.fr
  Local Query Share: **62.6667%**
  
  (Global Tranco Rank: 3711)
  

- **Rank 21:** radiofrance.fr
  Local Query Share: **62.4473%**
  
  (Global Tranco Rank: 3561)
  

- **Rank 22:** lefigaro.fr
  Local Query Share: **59.0734%**
  
  (Global Tranco Rank: 813)


- **Rank 23:** tf1.fr
  Local Query Share: **57.6877%**
  
  (Global Tranco Rank: 5851)
  

- **Rank 24:** paris.fr
  Local Query Share: **57.2973%**
  
  (Global Tranco Rank: 6130)
  

- **Rank 25:** meteociel.fr
  Local Query Share: **57.1429%**
  
  (Global Tranco Rank: 3765)

**Query 2 — Hosting analysis (AS and country hosting a domain)**

```cypher
// Query 2: Hosting Analysis — traces the AS and country hosting a given domain.
// The $domainName and $countryCode parameters must be provided during execution.
MATCH (d:DomainName {name: $domainName})
// Expand search to include the domain itself, its subdomains, and its hostnames
OPTIONAL MATCH (d)-[:RESOLVES_TO]->(ip1:IP)
OPTIONAL MATCH (d)<-[:PARENT*1..2]-(sub:DomainName)-[:RESOLVES_TO]->(ip2:IP)
OPTIONAL MATCH (d)-[:MANAGED_BY]->(h:HostName)-[:RESOLVES_TO]->(ip3:IP)

WITH coalesce(ip1, ip2, ip3) AS ip
WHERE ip IS NOT NULL

// Trace the hosting AS via the confirmed IYP path: IP -[:PART_OF]-> BGPPrefix <- [:ORIGINATE]- AS
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)

OPTIONAL MATCH (hostingAS)-[:NAME]->(n:Name)
OPTIONAL MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

WITH hostingAS, hostingCountry, collect(DISTINCT n.name)[0] AS hostingASName
RETURN DISTINCT
       hostingAS.asn AS hostingASN,
       hostingASName,
       hostingCountry.country_code AS hostingASCountry,
       (hostingCountry.country_code = $countryCode) AS isHostedLocally
LIMIT 10;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Hosting Infrastructure Analysis for service-public.fr

This query investigates the physical and logical location of the server hosting the domain **service-public.fr**.
- **Digital Sovereignty:** Local hosting ensures data remains within national jurisdiction and reduces latency.
- **Resilience Risk:** Hosting critical government services abroad creates dependencies on international transit and foreign legal frameworks.


**Hosting Details:**


- **Hosting Provider:** DISIC-RIE-AS LA DIRECTION INTERMINISTERIELLE DU NUMERIQUE (AS60855)
- **Location:** FR
  
  
  ✅ **Status:** LOCALLY HOSTED. This contributes to high digital sovereignty and resilience.
  

- **Hosting Provider:** OUTSCALE Outscale SASU (AS50624)
- **Location:** FR
  
  
  ✅ **Status:** LOCALLY HOSTED. This contributes to high digital sovereignty and resilience.
  

- **Hosting Provider:** CELESTE-AS CELESTE SAS (AS34177)
- **Location:** FR
  
  
  ✅ **Status:** LOCALLY HOSTED. This contributes to high digital sovereignty and resilience.

**Query 3 — RPKI status of a hosting AS**

```cypher
// Query 3: RPKI Status
MATCH (hostingAS:AS {asn: $hostingASN})-[:ORIGINATE]->(p:Prefix)
MATCH (p)-[:CATEGORIZED]->(t:Tag)
WHERE t.label STARTS WITH 'RPKI'
RETURN t.label AS rpkiStatus,
       count(p) AS numberOfPrefixes
ORDER BY numberOfPrefixes DESC;
```

> **Output:**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Routing Security (RPKI) Status for AS3215

This metric evaluates the routing hygiene of the Autonomous System hosting the target service.
- **RPKI Valid:** The provider protects its IP prefixes against BGP hijacking.
- **RPKI NotFound/Invalid:** The infrastructure is vulnerable to routing attacks, which could make the e-government service unreachable.


**RPKI Status Distribution:**


- **RPKI Valid:** 1758 prefix(es)
  
  *(Secure)*
  

- **RPKI NotFound:** 212 prefix(es)
  
  *(Vulnerable)*

### 2.2.3 Peering Efficiency

**Query 1 — Peering efficiency ratio**

```cypher
// Calcule le ratio d'efficacité du peering pour un pays donné.
// Le paramètre $countryCode doit être fourni (ex: 'FR', 'SN').

MATCH (c:Country {country_code: $countryCode})

// 1. Compter le nombre total d'AS dans le pays
OPTIONAL MATCH (local_as:AS)-[:COUNTRY]->(c)
WITH c, count(DISTINCT local_as) AS totalASNs

// 2. Compter le nombre d'AS locaux membres d'au moins un IXP local
OPTIONAL MATCH (peering_as:AS)-[:COUNTRY]->(c)
MATCH (peering_as)-[:MEMBER_OF]->(ixp:IXP)-[:COUNTRY]->(c)
WITH totalASNs, count(DISTINCT peering_as) AS peeringASNs

// 3. Calculer le ratio (éviter la division par zéro)
RETURN
    totalASNs,
    peeringASNs,
    CASE
        WHEN totalASNs > 0 THEN toFloat(peeringASNs) / toFloat(totalASNs)
        ELSE 0.0
    END AS peeringEfficiencyRatio;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Peering Efficiency Ratio for FR

This metric measures the density of the local peering ecosystem. It calculates the ratio between the networks (ASes) participating in domestic IXPs and the total number of networks in the country. A high ratio (close to 100%) indicates a mature and resilient market, where local traffic is exchanged efficiently, reducing latency and dependence on international transit.


**Analysis Results:**

- Total number of ASes in the country: **2238**
- ASes participating in local peering: **376**
- Peering Efficiency Ratio: **16.8%**

**Query 2 — Domestic IXPs and their local AS members**

```cypher
// Lists domestic IXPs and their number of local AS members.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'NG', 'US').
MATCH (c:Country {country_code: $countryCode})
MATCH (ixp:IXP)-[:COUNTRY]->(c)
MATCH (local_as:AS)-[:COUNTRY]->(c)
MATCH (local_as)-[:MEMBER_OF]->(ixp)
RETURN id(ixp) AS ixpId,
       ixp.name AS ixpName,
       count(DISTINCT local_as) AS localMemberCount
ORDER BY localMemberCount DESC
LIMIT 15;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: Domestic IXP Density Ranking for FR

This analysis identifies all domestic Internet Exchange Points (IXPs) and ranks them by the number of local AS members. This reveals which IXPs are the most critical for the country's peering ecosystem and whether this ecosystem is distributed (multiple IXPs) or centralized (a single dominant IXP).


**Ranking of the 15 identified IXP(s) by local member count:**


- **Rank 1:** France-IX Paris (ID: 3654261)
  Number of local members: **235**

- **Rank 2:** Equinix Paris (ID: 3653469)
  Number of local members: **151**

- **Rank 3:** France-IX AURA (ID: 3654213)
  Number of local members: **59**

- **Rank 4:** nine (ID: 3653957)
  Number of local members: **48**

- **Rank 5:** France-IX Marseille (ID: 3653665)
  Number of local members: **37**

- **Rank 6:** Lillix (ID: 3653633)
  Number of local members: **32**

- **Rank 7:** Hopus (ID: 3654552)
  Number of local members: **27**

- **Rank 8:** SFINX (ID: 3653687)
  Number of local members: **19**

- **Rank 9:** BreizhIX (ID: 3654422)
  Number of local members: **18**

- **Rank 10:** AuvernIX (ID: 3653428)
  Number of local members: **12**

- **Rank 11:** DE-CIX Marseille (ID: 3654025)
  Number of local members: **10**

- **Rank 12:** EuroRhine-IX (ID: 3654000)
  Number of local members: **10**

- **Rank 13:** France-IX Lille (ID: 3654383)
  Number of local members: **10**

- **Rank 14:** BGP.Exchange - Paris (ID: 3654425)
  Number of local members: **10**

- **Rank 15:** Ouest.Network (ID: 3653506)
  Number of local members: **9**

**Query 3 — Local ASes not peering at any local IXP**

```cypher
// Identifies local ASNs that do not peer at any local IXP, ordered by importance.
// The $countryCode parameter must be provided at execution.
MATCH (c:Country {country_code: $countryCode})

// Find all local ASNs
MATCH (localAS:AS)-[:COUNTRY]->(c)

// Filter to keep only those NOT connected to a local IXP
WHERE NOT EXISTS {
  MATCH (localAS)-[:MEMBER_OF]->(:IXP)-[:COUNTRY]->(c)
}

// Get AS Rank to sort by importance (lower rank is more important)
OPTIONAL MATCH (localAS)-[r:RANK]->(:Ranking {name:'CAIDA ASRank'})
WITH localAS, r
OPTIONAL MATCH (localAS)-[:NAME]->(n:Name)

RETURN
    localAS.asn AS asn,
    collect(DISTINCT n.name)[0] AS asName,
    r.rank AS caidaRank
ORDER BY caidaRank ASC
LIMIT 20;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: High-Impact ASes Not Participating in Local Peering for FR

This analysis identifies local networks (ASes) that are not members of any domestic IXP. They are ranked by their global importance (via CAIDA ASRank, where a lower number means a bigger network) to reveal which missing players have the biggest impact on domestic peering efficiency. Incentivizing these players to joinlocal IXPs is a key action to improve resilience.


**Ranking of major non-participating ASes (by Global Rank):**


- **Rank 1:** TWELVE99 Arelion Sweden AB (AS1299)
  Global Rank (ASRank): **2**

- **Rank 2:** AS3215 Orange S.A. (AS3215)
  Global Rank (ASRank): **247**

- **Rank 3:** IXREACH BSO Network Solutions SAS (AS43531)
  Global Rank (ASRank): **375**

- **Rank 4:** BSOCOM BSO Network Solutions SAS (AS31216)
  Global Rank (ASRank): **376**

- **Rank 5:** NFORCE NForce Entertainment B.V. (AS43350)
  Global Rank (ASRank): **1530**

- **Rank 6:** BOUYGTEL-B2B Bouygues Telecom SA (AS12844)
  Global Rank (ASRank): **1945**

- **Rank 7:** HOLYCLOUD GENIUSWEER SAS (AS198831)
  Global Rank (ASRank): **2233**

- **Rank 8:** team_blue team.blue NV (AS48185)
  Global Rank (ASRank): **2251**

- **Rank 9:** STELOGY-INFRASTRUCTURE Nomotech SAS (AS39886)
  Global Rank (ASRank): **2272**

- **Rank 10:** ZEN-DPS - Zenlayer Inc (AS62610)
  Global Rank (ASRank): **2393**

- **Rank 11:** KOESIO-NETWORKS KOESIO Networks SAS (AS206120)
  Global Rank (ASRank): **2637**

- **Rank 12:** NLT-FR nLighten France SAS (AS31221)
  Global Rank (ASRank): **3139**

- **Rank 13:** VELIANET-AS velia.net Internetdienste GmbH (AS29066)
  Global Rank (ASRank): **3265**

- **Rank 14:** APPLIWAVE Eurofiber France SAS (AS200780)
  Global Rank (ASRank): **3396**

- **Rank 15:** AS-COMPLETEL Completel SAS (AS12670)
  Global Rank (ASRank): **3459**

- **Rank 16:** I2SNETWORK I2SNETWORK SAS (AS52073)
  Global Rank (ASRank): **3586**

- **Rank 17:** DAUPHIN-TELECOM - Dauphin Telecom (AS33392)
  Global Rank (ASRank): **4448**

- **Rank 18:** PLB-NET Stevan Durand--L'Hours t/a SLBCLOUD (AS215114)
  Global Rank (ASRank): **4680**

- **Rank 19:** ORANGE-BUSINESS-SERVICES-BENELUX Orange S.A. (AS5583)
  Global Rank (ASRank): **4729**

- **Rank 20:** IELO-B (AS57179)
  Global Rank (ASRank): **5079**

**Query 4 — IXP peering depth distribution**

```cypher
// Measures the depth of IXP peering — how many IXPs each local AS participates in.
// An AS peering at multiple IXPs has better redundancy and resilience.
// The $countryCode parameter must be provided at execution.
MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)

// Find local IXPs the AS is ACTUALLY a member of.
OPTIONAL MATCH (as)-[:MEMBER_OF]->(ixp:IXP)-[:COUNTRY]->(c)

WITH as, count(DISTINCT ixp) AS ixpMembershipCount
WHERE ixpMembershipCount > 0

// Group by membership count to show the distribution.
RETURN
    ixpMembershipCount AS numberOfIXPsMemberOf,
    count(DISTINCT as) AS numberOfASes
ORDER BY ixpMembershipCount DESC;
```

> **Output**

==================================================
✅ RAW RESULT RECEIVED FROM NEO4J
==================================================

==================================================
✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)
==================================================
Title: IXP Membership Depth Distribution for FR

This analysis shows how many local Autonomous Systems participate in multiple Internet Exchange Points simultaneously. ASes peering at more IXPs have greater redundancy and resilience. A country where many ASes join only one IXP has a more fragile peering ecosystem than one where ASes routinely multi-home across several IXPs.


**IXP Membership Depth:**

| IXPs Joined | Number of ASes |
|-------------|----------------|

| 12 | 1 |

| 9 | 1 |

| 6 | 10 |

| 5 | 7 |

| 4 | 19 |

| 3 | 47 |

| 2 | 97 |

| 1 | 194 |


**Interpretation:**

Rows with `numberOfIXPsMemberOf > 1` represent ASes with redundant IXP presence — a sign of a mature peering ecosystem. If most ASes appear only in the `1` row, the ecosystem is functional but not yet resilient against a single IXP outage.

# 3. Security

## 3.1 DNS Security

### 3.1.1 DNSSEC Adoption

**Query 1 — Top 25 most popular domains by DNS query share**

```cypher
// Retrieves the 25 most popular domains for a given country, based on the percentage of DNS queries.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
RETURN d.name AS domainName,
       q.value AS queryPercentage
ORDER BY queryPercentage DESC
LIMIT 25;
```

> **Output (25 record(s)):**

```json
[
  {
    "domainName": "akamaixbc.net",
    "queryPercentage": 100.0
  },
  {
    "domainName": "tik.porn",
    "queryPercentage": 95.66787
  },
  {
    "domainName": "adprime.com",
    "queryPercentage": 94.198324
  },
  {
    "domainName": "ameli.fr",
    "queryPercentage": 91.973244
  },
  {
    "domainName": "dfn.nl",
    "queryPercentage": 89.700806
  },
  {
    "domainName": "louvre.fr",
    "queryPercentage": 87.40458
  },
  {
    "domainName": "huffingtonpost.fr",
    "queryPercentage": 86.813187
  },
  {
    "domainName": "doctolib.fr",
    "queryPercentage": 82.938389
  },
  {
    "domainName": "bigcartel.com",
    "queryPercentage": 82.141071
  },
  {
    "domainName": "proofpoint.us",
    "queryPercentage": 81.818182
  },
  {
    "domainName": "leroymerlin.fr",
    "queryPercentage": 81.426814
  },
  {
    "domainName": "anlikaltinfiyatlari.com",
    "queryPercentage": 79.62963
  },
  {
    "domainName": "boursorama.com",
    "queryPercentage": 79.411765
  },
  {
    "domainName": "destentor.nl",
    "queryPercentage": 79.310345
  },
  {
    "domainName": "fti.net",
    "queryPercentage": 77.941176
  },
  {
    "domainName": "meteofrance.com",
    "queryPercentage": 77.483444
  },
  {
    "domainName": "airbus.com",
    "queryPercentage": 77.469671
  },
  {
    "domainName": "lepoint.fr",
    "queryPercentage": 76.404494
  },
  {
    "domainName": "nestlechinese.com",
    "queryPercentage": 75.409836
  },
  {
    "domainName": "ortb.net",
    "queryPercentage": 75.08067
  },
  {
    "domainName": "leboncoin.fr",
    "queryPercentage": 75.0
  },
  {
    "domainName": "impots.gouv.fr",
    "queryPercentage": 75.0
  },
  {
    "domainName": "telenor.se",
    "queryPercentage": 72.447889
  },
  {
    "domainName": "vinted.fr",
    "queryPercentage": 72.349061
  },
  {
    "domainName": "yggtorrent.org",
    "queryPercentage": 72.222222
  }
]
```

**Query 2 — Popular domains hosted on infrastructure in the target country**

```cypher
// Retrieves popular domains hosted on infrastructure in the target country via BGP prefix ownership.
// Uses the valid IYP path: AS (in country) -[:ORIGINATE]-> BGPPrefix <- [:PART_OF]- IP <- [:RESOLVES_TO]- DomainName
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(pfx:BGPPrefix)<-[:PART_OF]-(ip:IP)<-[:RESOLVES_TO]-(d:DomainName)
// Filter by Tranco ranking for popular domains only.
MATCH (d)-[r:RANK]->(rk:Ranking)
WHERE rk.name CONTAINS 'Tranco'
RETURN d.name AS domainName,
       r.rank AS popularityRank,
       as.asn AS hostingASN
ORDER BY r.rank ASC
LIMIT 25;
```

> **Output (0 record(s)):**

```json
[]
```

**Query 3 — List all relationship types in the graph (schema introspection)**

```cypher
MATCH ()-[r]->()
RETURN DISTINCT type(r)
ORDER BY type(r)
```

> **Output (27 record(s)):**

```json
[
  {
    "type(r)": "ALIAS_OF"
  },
  {
    "type(r)": "ALLOCATED"
  },
  {
    "type(r)": "ASSIGNED"
  },
  {
    "type(r)": "AVAILABLE"
  },
  {
    "type(r)": "CATEGORIZED"
  },
  {
    "type(r)": "CENSORED"
  },
  {
    "type(r)": "COUNTRY"
  },
  {
    "type(r)": "DEPENDS_ON"
  },
  {
    "type(r)": "EXTERNAL_ID"
  },
  {
    "type(r)": "LEGACY"
  },
  {
    "type(r)": "LOCATED_IN"
  },
  {
    "type(r)": "MANAGED_BY"
  },
  {
    "type(r)": "MEMBER_OF"
  },
  {
    "type(r)": "NAME"
  },
  {
    "type(r)": "ORIGINATE"
  },
  {
    "type(r)": "PARENT"
  },
  {
    "type(r)": "PART_OF"
  },
  {
    "type(r)": "PEERS_WITH"
  },
  {
    "type(r)": "POPULATION"
  },
  {
    "type(r)": "QUERIED_FROM"
  },
  {
    "type(r)": "RANK"
  },
  {
    "type(r)": "RESERVED"
  },
  {
    "type(r)": "RESOLVES_TO"
  },
  {
    "type(r)": "ROUTE_ORIGIN_AUTHORIZATION"
  },
  {
    "type(r)": "SIBLING_OF"
  }
]
// ... (2 more records omitted, 27 total)
```

---

### 3.1.2 DNSSEC Validation

**Query 1 — RPKI ROV adoption rate (routing hygiene proxy for DNSSEC)**

```cypher
// Calculates the RPKI Route Origin Validation (ROV) adoption rate as a routing hygiene proxy.
// Used here to contextualize DNSSEC validation: networks that validate routing origins
// are more likely to be operating secure, well-managed DNS infrastructure.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'DE', 'BR').
MATCH (c:Country {country_code: $countryCode})
// Counts the total number of ASes in the country.
OPTIONAL MATCH (as:AS)-[:COUNTRY]->(c)
WITH c, count(DISTINCT as) AS totalASNs
// Counts ASes that validate RPKI Route Origin (MANRS-equivalent proxy).
OPTIONAL MATCH (rpki_as:AS)-[:COUNTRY]->(c)
WHERE (rpki_as)-[:CATEGORIZED]->(:Tag {label: "Validating RPKI ROV"})
WITH totalASNs, count(DISTINCT rpki_as) AS rpkiValidatingASNs
RETURN
    rpkiValidatingASNs,
    totalASNs,
    CASE
        WHEN totalASNs > 0 THEN (toFloat(rpkiValidatingASNs) / totalASNs) * 100
        ELSE 0
    END AS rpkiValidationPercentage;
```

> **Output (1 record(s)):**

```json
[
  {
    "rpkiValidatingASNs": 143,
    "totalASNs": 2238,
    "rpkiValidationPercentage": 6.389633601429848
  }
]
```

**Query 2 — Top ASes by population served with RPKI validation status**

```cypher
MATCH (c:Country {country_code: $countryCode})<-[pop:POPULATION]-(as:AS)

OPTIONAL MATCH (as)-[:NAME]->(n:Name)

OPTIONAL MATCH (as)-[:CATEGORIZED]->(rpkiTag:Tag {label: "Validating RPKI ROV"})

WITH
    as,
    pop.percent AS populationServedPercentage,
    collect(DISTINCT n.name)[0] AS name,
    count(rpkiTag) > 0 AS isRpkiValidating

RETURN
    as.asn AS asn,
    name,
    populationServedPercentage,
    isRpkiValidating

ORDER BY populationServedPercentage DESC
LIMIT 10
```

> **Output (10 record(s)):**

```json
[
  {
    "asn": 3215,
    "name": "AS3215 Orange S.A.",
    "populationServedPercentage": 35.38051167179335,
    "isRpkiValidating": true
  },
  {
    "asn": 12322,
    "name": "PROXAD Free SAS",
    "populationServedPercentage": 18.649609448176673,
    "isRpkiValidating": true
  },
  {
    "asn": 5410,
    "name": "BOUYGTEL-ISP Bouygues Telecom SA",
    "populationServedPercentage": 17.747870947714453,
    "isRpkiValidating": false
  },
  {
    "asn": 15557,
    "name": "LDCOMNET Societe Francaise Du Radiotelephone - SFR SA",
    "populationServedPercentage": 17.522857472432,
    "isRpkiValidating": true
  },
  {
    "asn": 51207,
    "name": "FREEM Free Mobile SAS",
    "populationServedPercentage": 4.545856517745062,
    "isRpkiValidating": true
  },
  {
    "asn": 16276,
    "name": "OVH OVH SAS",
    "populationServedPercentage": 0.8547753793962675,
    "isRpkiValidating": true
  },
  {
    "asn": 63023,
    "name": "AS-GLOBALTELEHOST - GTHost",
    "populationServedPercentage": 0.7778947419995292,
    "isRpkiValidating": true
  },
  {
    "asn": 12876,
    "name": "AS12876 Scaleway SAS",
    "populationServedPercentage": 0.6916868077604803,
    "isRpkiValidating": true
  },
  {
    "asn": 51167,
    "name": "CONTABO Contabo GmbH",
    "populationServedPercentage": 0.323644195442315,
    "isRpkiValidating": true
  },
  {
    "asn": 31404,
    "name": "Lycatel-AS LYCATEL DISTRIBUTION UK LIMITED",
    "populationServedPercentage": 0.2571962786868061,
    "isRpkiValidating": true
  }
]
```

---

## 3.2 Enabling Technologies

### 3.2.1 HTTPS Adoption

**Query 1 — HTTPS adoption rate (Google ranking data)**

```cypher
MATCH (:Country {country_code: $countryCode})-[:COUNTRY {reference_org: 'Google'}]-(r:Ranking)-[rr:RANK]-(hn:HostName)
WITH COUNT(DISTINCT hn) as count_total

MATCH (:Country {country_code: $countryCode})-[:COUNTRY {reference_org: 'Google'}]-(r:Ranking)-[rr:RANK]-(hn:HostName)
WHERE rr.rank <= 1000000 AND rr.origin STARTS WITH 'https'
WITH count_total, COUNT(DISTINCT hn) as count_https  // <-- Correction ici : on garde count_total

RETURN 
       CASE 
           WHEN count_total = 0 THEN 0.0 
           ELSE (toFloat(count_https) / count_total) * 100.0 
       END AS https_adoption_rate,
       count_https,
       count_total
```

> **Output (1 record(s)):**

```json
[
  {
    "https_adoption_rate": 98.62266817296518,
    "count_https": 974246,
    "count_total": 987852
  }
]
```

**Query 2 — HTTPS adoption among locally queried domains**

```cypher
// HTTPS adoption among locally queried domains

MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
WITH count(DISTINCT d) AS totalQueried

MATCH (c:Country {country_code: $countryCode})<-[q2:QUERIED_FROM]-(d:DomainName)
MATCH (h:HostName)-[:PART_OF]->(d)
MATCH (u:URL)-[:PART_OF]->(h)

WHERE u.url STARTS WITH 'https'

WITH totalQueried,
     count(DISTINCT d) AS httpsDomains

RETURN
    totalQueried,
    httpsDomains AS httpsCount,
    httpsDomains AS resolvedDomains,
    CASE
        WHEN totalQueried = 0 THEN 0.0
        ELSE round((toFloat(httpsDomains) / totalQueried) * 100.0, 2)
    END AS httpsAdoptionRate
```

> **Output (1 record(s)):**

```json
[
  {
    "totalQueried": 7438,
    "httpsCount": 901,
    "resolvedDomains": 901,
    "httpsAdoptionRate": 12.11
  }
]
```

---

### 3.2.2 IPv6 Adoption

**Query 1 — IPv6 prefix adoption rate**

```cypher
// Calculates the percentage of AS in a country that announce IPv6 prefixes.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'BE', 'CA').
MATCH (c:Country {country_code: $countryCode})

// Find all BGP prefixes originated by AS in this country
MATCH (as:AS)-[:COUNTRY]->(c)
MATCH (as)-[:ORIGINATE]->(p:BGPPrefix)

// Count the total, and count those that are IPv6 (af = 6)
WITH c, 
     count(p) AS totalPrefixes,
     count(CASE WHEN p.af = 6 THEN p ELSE null END) AS ipv6Prefixes,
     count(CASE WHEN p.af = 4 THEN p ELSE null END) AS ipv4Prefixes

// Calculate the percentage
RETURN c.name AS country,
       totalPrefixes,
       ipv4Prefixes,
       ipv6Prefixes,
       CASE 
           WHEN totalPrefixes = 0 THEN 0 
           ELSE (toFloat(ipv6Prefixes) / totalPrefixes) * 100.0 
       END AS ipv6PrefixesPercentage
ORDER BY ipv6PrefixesPercentage DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalPrefixes": 89499,
    "ipv4Prefixes": 72344,
    "ipv6Prefixes": 17155,
    "ipv6PrefixesPercentage": 19.167811930859564
  }
]
```

**Query 2 — ASes without IPv6, ranked by importance**

```cypher
// Identifies AS in a country without IPv6 announcements, ranked by importance.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'BE', 'CA').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)

// Check for the existence of IPv6 announcements for this AS.
OPTIONAL MATCH (as)-[:ORIGINATE]->(p:Prefix)
WHERE p.prefix CONTAINS ':'

WITH as, count(p) AS ipv6PrefixCount
// Keep only AS that have NO IPv6 announcements.
WHERE ipv6PrefixCount = 0

// Retrieve the rank and customer cone size to evaluate the importance of the AS.
MATCH (as)-[r:RANK]->(rank:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

RETURN
    as.asn AS asn,
    n.name AS name,
    r['cone:numberAsns'] AS customerConeSize
ORDER BY customerConeSize DESC
LIMIT 15;
```

> **Output (15 record(s)):**

```json
[
  {
    "asn": 51706,
    "name": "France-IX Paris Route Servers",
    "customerConeSize": 16
  },
  {
    "asn": 51706,
    "name": "France-IX Paris RS",
    "customerConeSize": 16
  },
  {
    "asn": 51706,
    "name": "FRANCE-IX-PAR-AS",
    "customerConeSize": 16
  },
  {
    "asn": 51706,
    "name": "FRANCE-IX-PAR-AS France IX Services SASU",
    "customerConeSize": 16
  },
  {
    "asn": 12844,
    "name": "BOUYGTEL-B2B",
    "customerConeSize": 15
  },
  {
    "asn": 12844,
    "name": "Bouygues Telecom SA",
    "customerConeSize": 15
  },
  {
    "asn": 12844,
    "name": "BOUYGTEL-B2B Bouygues Telecom SA",
    "customerConeSize": 15
  },
  {
    "asn": 39886,
    "name": "NOMOTECH",
    "customerConeSize": 12
  },
  {
    "asn": 39886,
    "name": "STELOGY-INFRASTRUCTURE Nomotech SAS",
    "customerConeSize": 12
  },
  {
    "asn": 39886,
    "name": "Nomotech SAS",
    "customerConeSize": 12
  },
  {
    "asn": 197033,
    "name": "CPRO-AS",
    "customerConeSize": 8
  },
  {
    "asn": 197033,
    "name": "KOESIO NETWORKS",
    "customerConeSize": 8
  },
  {
    "asn": 197033,
    "name": "CPRO-AS KOESIO Networks SAS",
    "customerConeSize": 8
  },
  {
    "asn": 197033,
    "name": "CPRO-AS",
    "customerConeSize": 8
  },
  {
    "asn": 197033,
    "name": "KOESIO Networks SAS",
    "customerConeSize": 8
  }
]
```

**Query 3 — IPv6 population coverage rate (ITU methodology)**

```cypher
// IPv6 population coverage rate — measures what percentage of the country's population
// is served by ASes that announce at least one IPv6 prefix. This is the population-weighted
// metric aligned with ITU's IPv6 adoption measurement methodology.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'BE', 'CA').
MATCH (c:Country {country_code: $countryCode})<-[pop:POPULATION]-(as:AS)
WITH c, sum(pop.percent) AS totalCoveredPopulationPct

MATCH (c:Country {country_code: $countryCode})<-[pop2:POPULATION]-(as2:AS)
WHERE (as2)-[:ORIGINATE]->(:BGPPrefix {af: 6})
WITH c, totalCoveredPopulationPct, sum(pop2.percent) AS ipv6CoveredPopulationPct

RETURN c.name AS country,
       round(totalCoveredPopulationPct, 2)  AS totalCoveredPopulationPct,
       round(ipv6CoveredPopulationPct, 2)   AS ipv6CoveredPopulationPct,
       CASE
           WHEN totalCoveredPopulationPct = 0 THEN 0
           ELSE round((ipv6CoveredPopulationPct / totalCoveredPopulationPct) * 100.0, 2)
       END AS ipv6PopulationCoverageRate;
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalCoveredPopulationPct": 99.46,
    "ipv6CoveredPopulationPct": 99.42,
    "ipv6PopulationCoverageRate": 99.96
  }
]
```

---

## 3.3 Routing Hygiene

### 3.3.1 MANRS Score

**Query 1 — RPKI ROV adoption rate**

```cypher
// Calculates the RPKI Route Origin Validation (ROV) adoption rate for a country.
// This is the primary technical action promoted by MANRS (routing security best practices).
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNsInCountry

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(rpkiAS:AS)-[:CATEGORIZED]->(t:Tag {label: "Validating RPKI ROV"})
WITH totalASNsInCountry, count(DISTINCT rpkiAS) AS rpkiValidatingCount

RETURN
  totalASNsInCountry,
  rpkiValidatingCount,
  round(100.0 * rpkiValidatingCount / totalASNsInCountry, 2) AS adoptionRatePercentage;
```

> **Output (1 record(s)):**

```json
[
  {
    "totalASNsInCountry": 2238,
    "rpkiValidatingCount": 143,
    "adoptionRatePercentage": 6.39
  }
]
```

**Query 2 — ASes validating RPKI ROV, ranked by customer cone**

```cypher
// Lists ASes validating RPKI Route Origin (the core MANRS routing security action), ranked by importance.

MATCH (c:Country {country_code: $countryCode})
      <-[:COUNTRY]-
      (as:AS)
      -[:CATEGORIZED]->
      (:Tag {label: "Validating RPKI ROV"})

OPTIONAL MATCH (as)-[r:RANK]->(:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

WITH
    as,
    collect(DISTINCT n.name)[0] AS asName,
    r['cone:numberAsns'] AS customerConeSize

RETURN
    as.asn AS asn,
    asName,
    customerConeSize

ORDER BY customerConeSize DESC
LIMIT 20;
```

> **Output (20 record(s)):**

```json
[
  {
    "asn": 1299,
    "asName": "TWELVE99 Arelion Sweden AB",
    "customerConeSize": 41002
  },
  {
    "asn": 5511,
    "asName": "Opentransit Orange S.A.",
    "customerConeSize": 7818
  },
  {
    "asn": 8218,
    "asName": "NEO-ASN Zayo Infrastructure France SA",
    "customerConeSize": 265
  },
  {
    "asn": 29075,
    "asName": "IELO IELO-LIAZO SERVICES SAS",
    "customerConeSize": 203
  },
  {
    "asn": 3215,
    "asName": "AS3215 Orange S.A.",
    "customerConeSize": 203
  },
  {
    "asn": 30781,
    "asName": "JAGUAR-AS Free Pro SAS",
    "customerConeSize": 199
  },
  {
    "asn": 16276,
    "asName": "OVH OVH SAS",
    "customerConeSize": 119
  },
  {
    "asn": 15557,
    "asName": "LDCOMNET Societe Francaise Du Radiotelephone - SFR SA",
    "customerConeSize": 91
  },
  {
    "asn": 62000,
    "asName": "NETRIX-AS SERVERD SAS",
    "customerConeSize": 83
  },
  {
    "asn": 25369,
    "asName": "BANDWIDTH-AS Hydra Communications Ltd",
    "customerConeSize": 83
  },
  {
    "asn": 47160,
    "asName": "MOJI MOJI SAS",
    "customerConeSize": 56
  },
  {
    "asn": 49434,
    "asName": "FBWNETWORKS FBW NETWORKS SAS",
    "customerConeSize": 51
  },
  {
    "asn": 29169,
    "asName": "GANDI-AS GANDI SAS",
    "customerConeSize": 37
  },
  {
    "asn": 34019,
    "asName": "HIVANE Hivane Association",
    "customerConeSize": 32
  },
  {
    "asn": 39180,
    "asName": "LASOTEL LASOTEL SAS",
    "customerConeSize": 26
  },
  {
    "asn": 63023,
    "asName": "AS-GLOBALTELEHOST - GTHost",
    "customerConeSize": 23
  },
  {
    "asn": 8309,
    "asName": "SIPARTECH SIPARTECH SAS",
    "customerConeSize": 22
  },
  {
    "asn": 212815,
    "asName": "AS-DYJIX Dyjix SAS",
    "customerConeSize": 17
  },
  {
    "asn": 46475,
    "asName": "LIMESTONENETWORKS - Limestone Networks, Inc.",
    "customerConeSize": 14
  },
  {
    "asn": 2027,
    "asName": "MilkyWan MilkyWan Association",
    "customerConeSize": 13
  }
]
```

**Query 3 — Routing hygiene breakdown (RPKI & IRR status of prefixes)**

```cypher
// Routing hygiene breakdown based on prefixes originated by ASes in the country.
// Measures RPKI and IRR status of announced prefixes.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').

MATCH (c:Country {country_code: $countryCode})
      <-[:COUNTRY]-
      (as:AS)
      -[:ORIGINATE]->
      (p:BGPPrefix)

MATCH (p)-[:CATEGORIZED]->(t:Tag)

WHERE t.label IN [
    'RPKI Valid',
    'RPKI Invalid',
    'RPKI NotFound',
    'IRR Valid',
    'IRR Invalid',
    'IRR NotFound'
]

RETURN
    t.label AS routingHygieneAction,
    count(DISTINCT p) AS implementingASNs
ORDER BY implementingASNs DESC;
```

> **Output (6 record(s)):**

```json
[
  {
    "routingHygieneAction": "IRR Valid",
    "implementingASNs": 12850
  },
  {
    "routingHygieneAction": "RPKI Valid",
    "implementingASNs": 12106
  },
  {
    "routingHygieneAction": "RPKI NotFound",
    "implementingASNs": 3131
  },
  {
    "routingHygieneAction": "IRR NotFound",
    "implementingASNs": 351
  },
  {
    "routingHygieneAction": "IRR Invalid",
    "implementingASNs": 270
  },
  {
    "routingHygieneAction": "RPKI Invalid",
    "implementingASNs": 8
  }
]
```

**Query 4 — MANRS Action 1: Route Filtering (IRR Valid rate)**

```cypher
// MANRS Action 1: Route Filtering — measures the IRR Valid route registration rate.
// IRR (Internet Routing Registry) registration is the technical prerequisite for
// route filtering, which is MANRS Action 1. An operator with IRR-valid prefixes has
// registered its route announcements, enabling peers to filter based on authoritative data.
// Note: IRR Valid is a tag on BGPPrefix nodes (not AS nodes directly).
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNs

// Count ASes that have at least one IRR-valid BGP prefix.
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(irrAS:AS)-[:ORIGINATE]->(p:BGPPrefix)-[:CATEGORIZED]->(t:Tag {label: "IRR Valid"})
WITH totalASNs, count(DISTINCT irrAS) AS irrValidCount

RETURN
  totalASNs,
  irrValidCount,
  round(100.0 * irrValidCount / totalASNs, 2) AS irrValidRatePercentage;
```

> **Output (1 record(s)):**

```json
[
  {
    "totalASNs": 2238,
    "irrValidCount": 1441,
    "irrValidRatePercentage": 64.39
  }
]
```

**Query 5 — MANRS Action 3: Coordination (PeeringDB registration rate)**

```cypher
// MANRS Action 3: Coordination — measures PeeringDB network registration rate.
// PeeringDB registration is the primary evidence of MANRS Action 3 compliance:
// operators must publish accurate contact and routing policy information so that
// peers can coordinate during routing incidents. An AS with a PeeringDB entry
// is reachable, documented, and demonstrably open to coordination.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNs

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(pdbAS:AS)-[:EXTERNAL_ID]->(:PeeringdbNetID)
WITH totalASNs, count(DISTINCT pdbAS) AS peeringdbCount

RETURN
  totalASNs,
  peeringdbCount,
  round(100.0 * peeringdbCount / totalASNs, 2) AS coordinationRatePercentage;
```

> **Output (1 record(s)):**

```json
[
  {
    "totalASNs": 2238,
    "peeringdbCount": 556,
    "coordinationRatePercentage": 24.84
  }
]
```

---

### 3.3.2 Upstream Connections

**Query 1 — Transit providers ranked by CAIDA ASRank**

```cypher
// Identifies transit providers of a country and ranks them by CAIDA ASRank.

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(local_as:AS)

MATCH (local_as)-[:PEERS_WITH {rel: 1}]->(provider:AS)

WHERE NOT (provider)-[:COUNTRY]->(c)

WITH provider, count(DISTINCT local_as) AS local_clients

OPTIONAL MATCH (provider)-[r:RANK]->(:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (provider)-[:NAME]->(n:Name)

WITH
    provider,
    local_clients,
    r.rank AS caidaASRank,
    collect(DISTINCT n.name)[0] AS providerName

RETURN
    provider.asn AS providerASN,
    providerName,
    local_clients,
    caidaASRank

ORDER BY caidaASRank ASC, local_clients DESC
LIMIT 20;
```

> **Output (20 record(s)):**

```json
[
  {
    "providerASN": 6939,
    "providerName": "HURRICANE - Hurricane Electric LLC",
    "local_clients": 3,
    "caidaASRank": 7
  },
  {
    "providerASN": 9002,
    "providerName": "RETN-AS RETN Limited",
    "local_clients": 2,
    "caidaASRank": 11
  },
  {
    "providerASN": 1273,
    "providerName": "CW Vodafone Group PLC",
    "local_clients": 2,
    "caidaASRank": 14
  },
  {
    "providerASN": 7473,
    "providerName": "SINGTEL-AS-AP Singapore Telecommunications Ltd",
    "local_clients": 1,
    "caidaASRank": 15
  },
  {
    "providerASN": 4637,
    "providerName": "ASN-TELSTRA-GLOBAL Telstra Global",
    "local_clients": 2,
    "caidaASRank": 16
  },
  {
    "providerASN": 12389,
    "providerName": "ROSTELECOM-AS PJSC Rostelecom",
    "local_clients": 2,
    "caidaASRank": 17
  },
  {
    "providerASN": 37468,
    "providerName": "ANGOLA-CABLES",
    "local_clients": 1,
    "caidaASRank": 21
  },
  {
    "providerASN": 9498,
    "providerName": "BBIL-AP BHARTI Airtel Ltd.",
    "local_clients": 1,
    "caidaASRank": 22
  },
  {
    "providerASN": 7195,
    "providerName": "EDGEUNO S.A.S",
    "local_clients": 1,
    "caidaASRank": 23
  },
  {
    "providerASN": 3216,
    "providerName": "SOVAM-AS PJSC \"Vimpelcom\"",
    "local_clients": 1,
    "caidaASRank": 24
  },
  {
    "providerASN": 58453,
    "providerName": "CMI-INT-HK China Mobile International Limited",
    "local_clients": 2,
    "caidaASRank": 26
  },
  {
    "providerASN": 20485,
    "providerName": "TRANSTELECOM Joint Stock Company TransTeleCom",
    "local_clients": 1,
    "caidaASRank": 27
  },
  {
    "providerASN": 31133,
    "providerName": "MF-MGSM-AS PJSC MegaFon",
    "local_clients": 1,
    "caidaASRank": 28
  },
  {
    "providerASN": 52320,
    "providerName": "GlobeNet Cabos Submarinos Colombia, S.A.S.",
    "local_clients": 1,
    "caidaASRank": 30
  },
  {
    "providerASN": 7922,
    "providerName": "COMCAST-7922 - Comcast Cable Communications, LLC",
    "local_clients": 2,
    "caidaASRank": 36
  },
  {
    "providerASN": 33891,
    "providerName": "CORE-BACKBONE Core-Backbone GmbH",
    "local_clients": 1,
    "caidaASRank": 37
  },
  {
    "providerASN": 52468,
    "providerName": "UFINET PANAMA S.A.",
    "local_clients": 2,
    "caidaASRank": 38
  },
  {
    "providerASN": 4826,
    "providerName": "VOCUS-BACKBONE-AS Vocus Connect International Backbone",
    "local_clients": 1,
    "caidaASRank": 41
  },
  {
    "providerASN": 15412,
    "providerName": "FLAG-AS FLAG TELECOM UK LIMITED",
    "local_clients": 1,
    "caidaASRank": 43
  },
  {
    "providerASN": 8220,
    "providerName": "COLT COLT Technology Services Group Limited",
    "local_clients": 2,
    "caidaASRank": 44
  }
]
```

**Query 2 — Provider tier distribution**

```cypher
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(local_as:AS)
MATCH (local_as)-[:PEERS_WITH {rel: 1}]->(provider:AS)
WHERE NOT (provider)-[:COUNTRY]->(c)

WITH DISTINCT provider

OPTIONAL MATCH (provider)-[r:RANK]->(:Ranking {name: 'CAIDA ASRank'})

WITH CASE
    WHEN r.rank IS NULL THEN 'E) Unranked'
    WHEN r.rank <= 100 THEN 'A) Top 100 (Internet Core)'
    WHEN r.rank <= 500 THEN 'B) Top 101-500 (Major)'
    WHEN r.rank <= 2000 THEN 'C) Top 501-2000 (Important)'
    ELSE 'D) Beyond 2000 (Regional/Niche)'
END AS providerTier

RETURN
    providerTier,
    count(*) AS numberOfProviders
ORDER BY providerTier;
```

> **Output (5 record(s)):**

```json
[
  {
    "providerTier": "A) Top 100 (Internet Core)",
    "numberOfProviders": 51
  },
  {
    "providerTier": "B) Top 101-500 (Major)",
    "numberOfProviders": 187
  },
  {
    "providerTier": "C) Top 501-2000 (Important)",
    "numberOfProviders": 417
  },
  {
    "providerTier": "D) Beyond 2000 (Regional/Niche)",
    "numberOfProviders": 2429
  },
  {
    "providerTier": "E) Unranked",
    "numberOfProviders": 74
  }
]
```

**Query 3 — Concentration of upstream providers**

```cypher
// Concentration of upstream providers

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as_fr:AS)

MATCH (as_fr)-[:PEERS_WITH]-(peer:AS)

MATCH (peer)-[:COUNTRY]->(peer_country:Country)

WHERE peer_country <> c

WITH
    peer,
    collect(DISTINCT peer_country.country_code)[0] AS upstreamCountry,
    count(DISTINCT as_fr) AS connectedDomesticClients

RETURN
    peer.asn AS upstreamAS,
    upstreamCountry,
    connectedDomesticClients

ORDER BY connectedDomesticClients DESC
LIMIT 10
```

> **Output (10 record(s)):**

```json
[
  {
    "upstreamAS": 174,
    "upstreamCountry": "US",
    "connectedDomesticClients": 343
  },
  {
    "upstreamAS": 6939,
    "upstreamCountry": "US",
    "connectedDomesticClients": 311
  },
  {
    "upstreamAS": 25091,
    "upstreamCountry": "CH",
    "connectedDomesticClients": 296
  },
  {
    "upstreamAS": 24482,
    "upstreamCountry": "SG",
    "connectedDomesticClients": 272
  },
  {
    "upstreamAS": 49544,
    "upstreamCountry": "NL",
    "connectedDomesticClients": 268
  },
  {
    "upstreamAS": 1828,
    "upstreamCountry": "US",
    "connectedDomesticClients": 261
  },
  {
    "upstreamAS": 36236,
    "upstreamCountry": "US",
    "connectedDomesticClients": 257
  },
  {
    "upstreamAS": 8298,
    "upstreamCountry": "CH",
    "connectedDomesticClients": 251
  },
  {
    "upstreamAS": 1239,
    "upstreamCountry": "US",
    "connectedDomesticClients": 246
  },
  {
    "upstreamAS": 39120,
    "upstreamCountry": "IT",
    "connectedDomesticClients": 243
  }
]
```

**Query 4 — Diversity of upstream peers**

```cypher
// Diversity of upstream peers

// Finds the country and its AS
MATCH (c:Country {country_code: $countryCode})
MATCH (c)<-[:COUNTRY]-(as_fr:AS)

// Finds all peers of these AS
MATCH (as_fr)-[:PEERS_WITH]-(peer:AS)

// Finds the country of these peers
MATCH (peer)-[:COUNTRY]->(peer_country:Country)

// Filters to keep only EXTERNAL peers
WHERE peer_country <> c

// Counts domestic AS and unique external peers
RETURN c.name AS country,
       count(DISTINCT as_fr) AS domesticOperators,
       count(DISTINCT peer) AS uniqueExternalPeers
ORDER BY uniqueExternalPeers DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "domesticOperators": 1015,
    "uniqueExternalPeers": 10675
  }
]
```

**Query 5 — Presence in international IXPs**

```cypher
// Presence in international IXPs

// Finds the country and its AS
MATCH (c:Country {country_code: $countryCode})
MATCH (c)<-[:COUNTRY]-(as_fr:AS)

// Finds the IXPs they are members of
MATCH (as_fr)-[:MEMBER_OF]->(ixp:IXP)

// Finds the country of the IXP
MATCH (ixp)-[:COUNTRY]->(ixp_country:Country)

// Filters to keep only IXPs abroad
WHERE ixp_country <> c

// Counts
RETURN c.name AS country,
       count(DISTINCT ixp) AS uniqueInternationalIXPs,
       count(DISTINCT as_fr) AS connectedInternationalOperators
ORDER BY connectedInternationalOperators DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "uniqueInternationalIXPs": 177,
    "connectedInternationalOperators": 137
  }
]
```

---

## 3.4 Security Threat

### 3.4.1 Cybersecurity Index Score

**Query 1 — RPKI prefix coverage rate**

```cypher
// RPKI prefix coverage rate — measures what percentage of a country's BGP prefixes
// have RPKI-valid Route Origin Authorizations (ROAs).
// Uses the IYP CATEGORIZED → Tag pattern (confirmed working schema).
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(p:BGPPrefix)
WITH c, count(DISTINCT p) AS totalPrefixes

// Count prefixes that have an RPKI Valid tag (i.e., covered by a valid ROA).
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as2:AS)-[:ORIGINATE]->(p2:BGPPrefix)-[:CATEGORIZED]->(t:Tag {label: "RPKI Valid"})
WITH c, totalPrefixes, count(DISTINCT p2) AS rpkiValidPrefixes

RETURN c.name AS country,
       totalPrefixes,
       rpkiValidPrefixes,
       CASE
           WHEN totalPrefixes = 0 THEN 0
           ELSE round((toFloat(rpkiValidPrefixes) / totalPrefixes) * 100.0, 2)
       END AS rpkiCoveragePercentage
ORDER BY rpkiCoveragePercentage DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalPrefixes": 15996,
    "rpkiValidPrefixes": 12106,
    "rpkiCoveragePercentage": 75.68
  }
]
```

**Query 2 — PeeringDB presence rate (coordination metric)**

```cypher
// Measures the PeeringDB presence rate of ASes in a country.
// A PeeringDB entry indicates a network is organized, documented, and open to coordination.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)
WITH c, collect(DISTINCT as) AS allASes

// Unwind and check for the presence of a PeeringDB ID
UNWIND allASes AS as
OPTIONAL MATCH (as)-[:EXTERNAL_ID]->(pdb:PeeringdbNetID)

WITH c,
     count(as) AS totalAS,
     count(pdb) AS asWithPeeringDB

// Calculate the percentage
RETURN c.name AS country,
       totalAS,
       asWithPeeringDB,
       CASE
           WHEN totalAS = 0 THEN 0
           ELSE (toFloat(asWithPeeringDB) / totalAS) * 100.0
       END AS coordinationPercentage
ORDER BY coordinationPercentage DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalAS": 2238,
    "asWithPeeringDB": 556,
    "coordinationPercentage": 24.84361036639857
  }
]
```

**Query 3 — Internet hegemony concentration**

```cypher
// Internet hegemony concentration

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(localAS:AS)
MATCH (localAS)-[d:DEPENDS_ON]->(provider:AS)

WHERE d.hege > 0.05
  AND NOT (provider)-[:COUNTRY]->(c)

WITH provider,
     count(DISTINCT localAS) AS dependentLocalASes,
     avg(d.hege)             AS avgHegemonyScore,
     max(d.hege)             AS maxHegemonyScore

OPTIONAL MATCH (provider)-[:NAME]->(n:Name)
OPTIONAL MATCH (provider)-[:COUNTRY]->(providerCountry:Country)

WITH provider,
     collect(DISTINCT n.name)[0] AS providerName,
     collect(DISTINCT providerCountry.country_code)[0] AS providerCountry,
     dependentLocalASes,
     avgHegemonyScore,
     maxHegemonyScore

RETURN
       provider.asn AS providerASN,
       providerName,
       providerCountry,
       dependentLocalASes,
       round(avgHegemonyScore, 4) AS avgHegemonyScore,
       round(maxHegemonyScore, 4) AS maxHegemonyScore

ORDER BY dependentLocalASes DESC,
         avgHegemonyScore DESC
LIMIT 10
```

> **Output (10 record(s)):**

```json
[
  {
    "providerASN": 6939,
    "providerName": "HURRICANE - Hurricane Electric LLC",
    "providerCountry": "US",
    "dependentLocalASes": 768,
    "avgHegemonyScore": 0.3594,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 174,
    "providerName": "COGENT-174 - Cogent Communications, LLC",
    "providerCountry": "US",
    "dependentLocalASes": 448,
    "avgHegemonyScore": 0.4225,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 3356,
    "providerName": "LEVEL3 - Level 3 Parent, LLC",
    "providerCountry": "US",
    "dependentLocalASes": 256,
    "avgHegemonyScore": 0.2509,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 6762,
    "providerName": "SEABONE-NET TELECOM ITALIA SPARKLE S.p.A.",
    "providerCountry": "IT",
    "dependentLocalASes": 235,
    "avgHegemonyScore": 0.1929,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 6461,
    "providerName": "ZAYO-6461 - Zayo Bandwidth",
    "providerCountry": "US",
    "dependentLocalASes": 138,
    "avgHegemonyScore": 0.3714,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 8220,
    "providerName": "COLT COLT Technology Services Group Limited",
    "providerCountry": "GB",
    "dependentLocalASes": 103,
    "avgHegemonyScore": 0.6608,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 137409,
    "providerName": "GSLNETWORKS-AS-AP GSL Networks Pty LTD",
    "providerCountry": "AU",
    "dependentLocalASes": 95,
    "avgHegemonyScore": 0.33,
    "maxHegemonyScore": 0.85
  },
  {
    "providerASN": 3257,
    "providerName": "GTT-BACKBONE GTT Communications Inc.",
    "providerCountry": "US",
    "dependentLocalASes": 90,
    "avgHegemonyScore": 0.3257,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 2914,
    "providerName": "NTT-DATA-2914 - NTT America, Inc.",
    "providerCountry": "US",
    "dependentLocalASes": 75,
    "avgHegemonyScore": 0.1849,
    "maxHegemonyScore": 1.0
  },
  {
    "providerASN": 29222,
    "providerName": "Infomaniak-AS Infomaniak Network SA",
    "providerCountry": "CH",
    "dependentLocalASes": 64,
    "avgHegemonyScore": 0.1167,
    "maxHegemonyScore": 0.125
  }
]
```

---

### 3.4.2 DDoS Protection

**Query 1 — CDN ASes in the country**

```cypher
// Lists Content Delivery Network (CDN) ASes located in the target country.
// Uses the "Content Delivery Network" tag from the IYP dataset.
//
// Problem solved:
// An AS can have multiple Name nodes attached (e.g. OVH, OVHcloud, OVH SAS),
// which previously caused duplicate rows in the output.
// We use collect(DISTINCT n.name)[0] to select a single representative name
// for each ASN and avoid duplicates.
//
// The parameter $countryCode must be provided during execution
// (e.g., 'FR', 'SN', 'JP').

// Step 1: Find all ASes belonging to the target country.
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)

// Step 2: Keep only ASes tagged as Content Delivery Networks (CDNs).
MATCH (as)-[:CATEGORIZED]->(:Tag {label: 'Content Delivery Network'})

// Step 3: Retrieve AS names.
// OPTIONAL MATCH is used because some ASes may not have a Name node.
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

// Step 4: Group results by ASN and collect all attached names.
// DISTINCT prevents duplicate names.
// [0] selects the first available name as the representative display name.
WITH as,
     collect(DISTINCT n.name)[0] AS cdnName

// Step 5: Return one row per CDN ASN.
RETURN
       as.asn AS cdnASN,
       cdnName

// Step 6: Sort alphabetically by CDN name.
ORDER BY cdnName;
```

> **Output (3 record(s)):**

```json
[
  {
    "cdnASN": 29264,
    "cdnName": "CDN-CANAL-PLUS"
  },
  {
    "cdnASN": 49477,
    "cdnName": "E-TF1 E-TF1 SAS"
  },
  {
    "cdnASN": 16276,
    "cdnName": "OVH OVH SAS"
  }
]
```

**Query 2 — CDN population coverage**

```cypher
// Measures the percentage of the country's population served by CDN ASes.
// The parameter $countryCode must be provided (e.g., 'FR', 'SN', 'JP').

MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)

MATCH (as)-[:CATEGORIZED]->(:Tag {label: 'Content Delivery Network'})

OPTIONAL MATCH (as)-[:NAME]->(n:Name)

// Collapse multiple Name nodes into a single representative name
WITH as,
     p.percent AS populationServedPercentage,
     collect(DISTINCT n.name)[0] AS cdnName

RETURN
       as.asn AS cdnASN,
       cdnName,
       populationServedPercentage

ORDER BY populationServedPercentage DESC;
```

> **Output (6 record(s)):**

```json
[
  {
    "cdnASN": 16276,
    "cdnName": "OVH OVH SAS",
    "populationServedPercentage": 0.8547753793962675
  },
  {
    "cdnASN": 13335,
    "cdnName": "CLOUDFLARENET - Cloudflare, Inc.",
    "populationServedPercentage": 0.21004564387110403
  },
  {
    "cdnASN": 21859,
    "cdnName": "ZEN-ECN",
    "populationServedPercentage": 0.1690633040975202
  },
  {
    "cdnASN": 16509,
    "cdnName": "AMAZON-02 - Amazon.com, Inc.",
    "populationServedPercentage": 0.13970076797768416
  },
  {
    "cdnASN": 60068,
    "cdnName": "CDN77 Datacamp Limited",
    "populationServedPercentage": 0.03531609767433955
  },
  {
    "cdnASN": 15169,
    "cdnName": "GOOGLE - Google LLC",
    "populationServedPercentage": 0.01993543357201414
  }
]
```

**Query 3 — CDN/DDoS protection of popular domains**

```cypher
MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)

WITH d, q.value AS queryPercentage
ORDER BY queryPercentage DESC
LIMIT 20

MATCH (d)<-[:PART_OF]-(h:HostName)
MATCH (h)-[:RESOLVES_TO]->(ip:IP)
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)
MATCH (hostAS:AS)-[:ORIGINATE]->(pfx)

MATCH (hostAS)-[:CATEGORIZED]->(cat:Tag)
WHERE cat.label IN ["Content Delivery Network","DDoS Mitigation"]

OPTIONAL MATCH (hostAS)-[:NAME]->(n:Name)

WITH
    d.name AS popularDomain,
    hostAS.asn AS hostingASN,
    collect(DISTINCT cat.label) AS protections,
    collect(DISTINCT n.name)[0] AS hostingName,
    max(queryPercentage) AS queryPercentage

RETURN DISTINCT
       popularDomain,
       hostingASN,
       hostingName,
       protections,
       queryPercentage
ORDER BY queryPercentage DESC
LIMIT 20;
```

> **Output (20 record(s)):**

```json
[
  {
    "popularDomain": "tik.porn",
    "hostingASN": 13335,
    "hostingName": "CLOUDFLARENET - Cloudflare, Inc.",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 95.66787
  },
  {
    "popularDomain": "tik.porn",
    "hostingASN": 199524,
    "hostingName": "GCORE G-Core Labs S.A.",
    "protections": [
      "DDoS Mitigation",
      "Content Delivery Network"
    ],
    "queryPercentage": 95.66787
  },
  {
    "popularDomain": "ameli.fr",
    "hostingASN": 16276,
    "hostingName": "OVH OVH SAS",
    "protections": [
      "DDoS Mitigation",
      "Content Delivery Network"
    ],
    "queryPercentage": 91.973244
  },
  {
    "popularDomain": "ameli.fr",
    "hostingASN": 13335,
    "hostingName": "CLOUDFLARENET - Cloudflare, Inc.",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 91.973244
  },
  {
    "popularDomain": "louvre.fr",
    "hostingASN": 16276,
    "hostingName": "OVH OVH SAS",
    "protections": [
      "DDoS Mitigation",
      "Content Delivery Network"
    ],
    "queryPercentage": 87.40458
  },
  {
    "popularDomain": "louvre.fr",
    "hostingASN": 13335,
    "hostingName": "CLOUDFLARENET - Cloudflare, Inc.",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 87.40458
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 270014,
    "hostingName": "GRUPO CG LIMITADA",
    "protections": [
      "Content Delivery Network"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 20764,
    "hostingName": "RASCOM-AS CJSC RASCOM",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 1299,
    "hostingName": "TWELVE99 Arelion Sweden AB",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 30844,
    "hostingName": "LIQUID-AS Liquid Telecommunications Ltd",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 14840,
    "hostingName": "BR.Digital Telecom",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 24482,
    "hostingName": "SGGS-AS-AP SG.GS",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "huffingtonpost.fr",
    "hostingASN": 9002,
    "hostingName": "RETN-AS RETN Limited",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 86.813187
  },
  {
    "popularDomain": "doctolib.fr",
    "hostingASN": 16509,
    "hostingName": "AMAZON-02 - Amazon.com, Inc.",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 82.938389
  },
  {
    "popularDomain": "bigcartel.com",
    "hostingASN": 13335,
    "hostingName": "CLOUDFLARENET - Cloudflare, Inc.",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 82.141071
  },
  {
    "popularDomain": "leroymerlin.fr",
    "hostingASN": 30844,
    "hostingName": "LIQUID-AS Liquid Telecommunications Ltd",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 81.426814
  },
  {
    "popularDomain": "leroymerlin.fr",
    "hostingASN": 14840,
    "hostingName": "BR.Digital Telecom",
    "protections": [
      "Content Delivery Network",
      "DDoS Mitigation"
    ],
    "queryPercentage": 81.426814
  },
  {
    "popularDomain": "leroymerlin.fr",
    "hostingASN": 24482,
    "hostingName": "SGGS-AS-AP SG.GS",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 81.426814
  },
  {
    "popularDomain": "leroymerlin.fr",
    "hostingASN": 9002,
    "hostingName": "RETN-AS RETN Limited",
    "protections": [
      "DDoS Mitigation"
    ],
    "queryPercentage": 81.426814
  },
  {
    "popularDomain": "leroymerlin.fr",
    "hostingASN": 270014,
    "hostingName": "GRUPO CG LIMITADA",
    "protections": [
      "Content Delivery Network"
    ],
    "queryPercentage": 81.426814
  }
]
```

**Query 4 — IXP diversity in the country**

```cypher
// 4. Diversity of Internet Exchange Points (IXP) in a country.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'DE', 'BR').
MATCH (c:Country {country_code: $countryCode})

// Find IXPs located in the country.
MATCH (ixp:IXP)-[:COUNTRY]->(c)

// Find ASes that are members of these IXPs.
MATCH (as:AS)-[:MEMBER_OF]->(ixp)

// Count the entities.
RETURN c.name AS country,
       count(DISTINCT ixp) AS numberOfIXPs,
       count(DISTINCT as) AS numberOfASMembers
ORDER BY numberOfIXPs DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "numberOfIXPs": 23,
    "numberOfASMembers": 754
  }
]
```

**Query 5 — Network monitoring density (RIPE Atlas probes)**

```cypher
// 3. Network Monitoring Density

// Find the country
MATCH (c:Country {country_code: $countryCode})

// Find probes located in this country
MATCH (p:AtlasProbe)
WHERE p.country_code = $countryCode
RETURN c.name AS country,
       count(DISTINCT p) AS numberOfAtlasProbes
ORDER BY numberOfAtlasProbes DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "numberOfAtlasProbes": 2668
  }
]
```

**Query 6 — RPKI coverage via ROA prefixes**

```cypher
MATCH (c:Country {country_code: $countryCode})
MATCH (c)<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)

WITH c, count(DISTINCT p) AS totalPrefixes

MATCH (c)<-[:COUNTRY]-(a2:AS)
MATCH (a2)-[:ROUTE_ORIGIN_AUTHORIZATION]->(rp:RPKIPrefix)
MATCH (rp)-[:PART_OF]->(p2:BGPPrefix)

WITH c,
     totalPrefixes,
     count(DISTINCT p2) AS coveredPrefixes

RETURN
       c.name AS country,
       totalPrefixes,
       coveredPrefixes,
       round(
           (toFloat(coveredPrefixes) / totalPrefixes) * 100.0,
           2
       ) AS rpkiCoveragePercentage;
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalPrefixes": 15996,
    "coveredPrefixes": 10352,
    "rpkiCoveragePercentage": 64.72
  }
]
```

---

### 3.4.3 Secure Internet Servers

**Query 1 — RPKI coverage of server-hosting prefixes**

```cypher
// 1. RPKI coverage rate of prefixes hosting servers
//
// Measures what percentage of server-hosting BGP prefixes
// are covered by at least one RPKI Route Origin Authorization (ROA).
//
// The parameter $countryCode must be provided during execution
// (e.g., 'FR', 'SN', 'JP').

// Step 1: Find all unique BGP prefixes hosting servers in the country.
MATCH (c:Country {country_code: $countryCode})

MATCH (h:HostName)-[:RESOLVES_TO]->(ip:IP)
MATCH (ip)-[:PART_OF]->(p:BGPPrefix)
MATCH (p)-[:COUNTRY]->(c)

WITH c, collect(DISTINCT p) AS allServerPrefixes

// Step 2: Check which prefixes are covered by at least one RPKI prefix.
UNWIND allServerPrefixes AS prefix

OPTIONAL MATCH (prefix)<-[:PART_OF]-(rpki:RPKIPrefix)

// Step 3: Count total prefixes and covered prefixes.
// Count covered *prefixes*, not RPKIPrefix objects.
WITH c,
     count(DISTINCT prefix) AS totalPrefixes,
     count(DISTINCT CASE WHEN rpki IS NOT NULL THEN prefix END) AS coveredPrefixes

// Step 4: Calculate coverage percentage.
RETURN c.name AS country,
       totalPrefixes,
       coveredPrefixes,
       CASE
           WHEN totalPrefixes = 0 THEN 0
           ELSE round((toFloat(coveredPrefixes) / totalPrefixes) * 100.0, 2)
       END AS rpkiCoveragePercentage

ORDER BY rpkiCoveragePercentage DESC;
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "totalPrefixes": 5418,
    "coveredPrefixes": 3667,
    "rpkiCoveragePercentage": 67.68
  }
]
```

**Query 2 — DNS infrastructure density**

```cypher
// 2. DNS infrastructure density — counts HostName nodes resolved to IPs in the country.
// Uses the confirmed IYP path: HostName -[:RESOLVES_TO]-> IP -[:PART_OF]-> BGPPrefix -[:COUNTRY]-> Country.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})

// Count distinct HostNames (acting as server identities) resolving to IPs located in this country.
MATCH (h:HostName)-[:RESOLVES_TO]->(ip:IP)-[:PART_OF]->(pfx:BGPPrefix)-[:COUNTRY]->(c)

// Find the AS that originates the prefix (i.e., the hosting operator).
MATCH (hostAS:AS)-[:ORIGINATE]->(pfx)
OPTIONAL MATCH (hostAS)-[:NAME]->(n:Name)

WITH c,
     count(DISTINCT h)      AS totalHostNames,
     count(DISTINCT hostAS)  AS hostingOperators

RETURN c.name          AS country,
       totalHostNames   AS dnsInfrastructureNodes,
       hostingOperators AS numberOfHostingOperators
ORDER BY dnsInfrastructureNodes DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "dnsInfrastructureNodes": 1197343,
    "numberOfHostingOperators": 1238
  }
]
```

**Query 3 — Diversity of operators hosting servers**

```cypher
// 3. Diversity of operators (AS) hosting servers
MATCH (c:Country {country_code: $countryCode})

// 1. Find servers (HostName) in the country (via IP/Prefix)
MATCH (h:HostName)-[:RESOLVES_TO]->(ip:IP)-[:PART_OF]->(p:BGPPrefix)-[:COUNTRY]->(c)

// 2. Find the AS announcing (originating) this prefix
//    (ASSUMPTION: :ORIGINATE is the relationship AS -> BGPPrefix)
MATCH (as:AS)-[:ORIGINATE]->(p)

// 3. (Optional) Ensure the AS is also based in this country
// MATCH (as)-[:COUNTRY]->(c)

// 4. Count
RETURN c.name AS country,
       count(DISTINCT h) AS numberOfServers,
       count(DISTINCT as) AS numberOfASOperators
ORDER BY numberOfASOperators DESC
```

> **Output (1 record(s)):**

```json
[
  {
    "country": "France",
    "numberOfServers": 1197343,
    "numberOfASOperators": 1238
  }
]
```

---

*Document generated on 2026-06-08. Contains 60 Cypher queries across 3 pillars, 10 sub-categories, and 20 metrics. All outputs executed against IYP with `countryCode = 'FR'` (France).*