# YPI Cypher Queries — Complete Reference

> All Cypher queries used for the YPI research, organized by pillar, sub-category, and metric. Each query is numbered in execution order. All outputs shown are for **France (`FR`)**.

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

> **Output (225 record(s)):**

```json
[
  {
    "DataCenter": "Telehouse - Paris 2 (Voltaire - Léon Frot)",
    "ColocatedASes": 347
  },
  {
    "DataCenter": "Digital Realty Marseille MRS1/2/3/4",
    "ColocatedASes": 212
  },
  {
    "DataCenter": "Equinix PA2 - Paris, Saint-Denis",
    "ColocatedASes": 141
  },
  {
    "DataCenter": "Equinix PA3 - Paris, Saint-Denis",
    "ColocatedASes": 120
  },
  {
    "DataCenter": "UltraEdge Lyon-Venissieux",
    "ColocatedASes": 82
  },
  {
    "DataCenter": "Digital Realty Paris PAR5",
    "ColocatedASes": 68
  },
  {
    "DataCenter": "Equinix PA6 - Paris, Condorcet",
    "ColocatedASes": 56
  },
  {
    "DataCenter": "Equinix PA5 - Paris, Victor Hugo",
    "ColocatedASes": 55
  },
  {
    "DataCenter": "Digital Realty Paris PAR2",
    "ColocatedASes": 53
  },
  {
    "DataCenter": "Equinix PA7 - Paris, Energy Park",
    "ColocatedASes": 49
  },
  {
    "DataCenter": "Telehouse - Paris 3 (Magny)",
    "ColocatedASes": 48
  },
  {
    "DataCenter": "OPCORE - DC2 / PAR2",
    "ColocatedASes": 47
  },
  {
    "DataCenter": "Equinix PA4 - Paris, Pantin",
    "ColocatedASes": 47
  },
  {
    "DataCenter": "ETIX Lille #2",
    "ColocatedASes": 46
  },
  {
    "DataCenter": "UltraEdge Paris - Courbevoie",
    "ColocatedASes": 41
  },
  {
    "DataCenter": "UltraEdge Strasbourg",
    "ColocatedASes": 41
  },
  {
    "DataCenter": "Digital Realty Paris PAR1",
    "ColocatedASes": 34
  },
  {
    "DataCenter": "Global Switch Paris",
    "ColocatedASes": 31
  },
  {
    "DataCenter": "UltraEdge Bordeaux",
    "ColocatedASes": 28
  },
  {
    "DataCenter": "ETIX Lyon #1",
    "ColocatedASes": 27
  },
  {
    "DataCenter": "Free Pro - Marseille - MRS1",
    "ColocatedASes": 27
  },
  {
    "DataCenter": "Cogent Rennes",
    "ColocatedASes": 26
  },
  {
    "DataCenter": "OPCORE - DC3 / PAR3",
    "ColocatedASes": 25
  },
  {
    "DataCenter": "Free Pro - Lyon - Rock",
    "ColocatedASes": 23
  },
  {
    "DataCenter": "Cogent Grenoble",
    "ColocatedASes": 21
  },
  {
    "DataCenter": "DATA4 Paris Marcoussis - PAR1",
    "ColocatedASes": 21
  },
  {
    "DataCenter": "Eurofiber DC - TLS00",
    "ColocatedASes": 21
  },
  {
    "DataCenter": "Digital Realty Paris PAR7",
    "ColocatedASes": 20
  },
  {
    "DataCenter": "Treefaz Jeûneurs",
    "ColocatedASes": 20
  },
  {
    "DataCenter": "ETIX Lille #3",
    "ColocatedASes": 20
  },
  {
    "DataCenter": "ETIX Nantes #1",
    "ColocatedASes": 20
  },
  {
    "DataCenter": "dc2scale PAR2 (Vélizy-Villacoublay)",
    "ColocatedASes": 20
  },
  {
    "DataCenter": "Telehouse - Paris 1 (Jeûneurs)",
    "ColocatedASes": 19
  },
  {
    "DataCenter": "nLighten Lyon LYS1",
    "ColocatedASes": 19
  },
  {
    "DataCenter": "Digital Realty Paris PAR3",
    "ColocatedASes": 18
  },
  {
    "DataCenter": "Cogent Toulouse",
    "ColocatedASes": 18
  },
  {
    "DataCenter": "Cogent Nantes",
    "ColocatedASes": 17
  },
  {
    "DataCenter": "Free Pro - Limonest",
    "ColocatedASes": 16
  },
  {
    "DataCenter": "Orange Business - La Fabrique [Grenoble]",
    "ColocatedASes": 15
  },
  {
    "DataCenter": "nLighten Sophia Antipolis NCE1",
    "ColocatedASes": 15
  },
  {
    "DataCenter": "Cogent Montpellier",
    "ColocatedASes": 15
  },
  {
    "DataCenter": "Equinix PA10 - Paris, Saint-Denis",
    "ColocatedASes": 14
  },
  {
    "DataCenter": "Digital Realty Paris PAR6",
    "ColocatedASes": 14
  },
  {
    "DataCenter": "ETIX Lille #1",
    "ColocatedASes": 13
  },
  {
    "DataCenter": "nLighten Besancon MLH1",
    "ColocatedASes": 13
  },
  {
    "DataCenter": "Level(3) Paris (Le Capitole)",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "Penta Infra Paris PAR01",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "ETIX Nantes #2",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "Telco Center",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "ETIX Montpellier #1",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "Cogent Strasbourg",
    "ColocatedASes": 12
  },
  {
    "DataCenter": "dc2scale PAR3 (Vélizy-Villacoublay)",
    "ColocatedASes": 11
  },
  {
    "DataCenter": "ETIX Toulouse #1",
    "ColocatedASes": 11
  },
  {
    "DataCenter": "Cogent Bordeaux",
    "ColocatedASes": 11
  },
  {
    "DataCenter": "Cogent Poitiers",
    "ColocatedASes": 10
  },
  {
    "DataCenter": "TDF Datacenter Rennes Cesson",
    "ColocatedASes": 10
  },
  {
    "DataCenter": "Cogent Dijon",
    "ColocatedASes": 10
  },
  {
    "DataCenter": "CC IN2P3",
    "ColocatedASes": 10
  },
  {
    "DataCenter": "Cogent Rouen",
    "ColocatedASes": 9
  },
  {
    "DataCenter": "Oceanet Armor B",
    "ColocatedASes": 9
  },
  {
    "DataCenter": "Ikoula IKDC1",
    "ColocatedASes": 9
  },
  {
    "DataCenter": "Datacenter NEXEREN",
    "ColocatedASes": 8
  },
  {
    "DataCenter": "Cogent Tours",
    "ColocatedASes": 8
  },
  {
    "DataCenter": "Cogent Velizy",
    "ColocatedASes": 8
  },
  {
    "DataCenter": "nLighten Strasbourg SXB1",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "UltraEdge Rennes",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "Equinix BX1 - Bordeaux",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "moji1",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "Cogent Nice",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "Equinix PA1 - Paris, Roissy",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "ETIX Nantes #3",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "Cogent Lille",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "TDF Datacenter Bordeaux Bouliac",
    "ColocatedASes": 7
  },
  {
    "DataCenter": "Dyjix",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "nLighten Paris PAR2",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "Digital Realty Paris PAR8",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "OPCORE - DC5 / PAR5",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "TDF Datacenter Aix Marseille",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "Datacenter Cyrès",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "Green Data - Nanterre",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "ETIX Paris #3",
    "ColocatedASes": 6
  },
  {
    "DataCenter": "Cogent Antibes",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "ETIX Paris #1",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "Neuf Cesson",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "Axione Lotim Telecom",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "Digital Realty Paris PAR4",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "Axione ADTIM",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "UltraEdge Rezé",
    "ColocatedASes": 5
  },
  {
    "DataCenter": "Maxnod",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "UltraEdge Toulouse",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "Orange / Val de Rueil",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "Hotel des Telecoms",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "UltraEdge Montpellier",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "TDF Datacenter Lille Lambersart",
    "ColocatedASes": 4
  },
  {
    "DataCenter": "10 Rue des Frères Peuge",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Salamandre",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "MCI/Verizon Paris St Denis",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Prosoluce SG-1 Datacenter",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Advanced MedioMatrix",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Hexanet - DC Sabine",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Montpellier Internet Telecom Datacenter",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "LASOTEL PIXEL",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "EXA Edge DC Nice",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "UltraEdge Grenoble",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Comarch France #1",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "COLT DC Paris II",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "APPLIWAVE - CBO",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "ITinSell Cloud Datacenter",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Haute-Saône Numérique",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Axione Limousin",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Hexanet - DC Roland",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "Aqua Ray Aurora",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "D-LAKE",
    "ColocatedASes": 3
  },
  {
    "DataCenter": "UltraEdge Lille",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Ecocenter",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "dc2scale PAR4x (Meudon)",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Somme-numerique DC1",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "XL360",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Completel Val de Reuil",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Cassin1",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Ad Valem Technologies - France (Saint-Denis)",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "DTIX Dijon",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "TDF Datacenter Paris Fort de Romainville",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Celeste Marilyn",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "PoP Faraday (Rouen)",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Techcrea Valenciennes",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "TAS Sophia",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "XSALTO Grenoble",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "dc2scale PAR5 (Vélizy-Villacoublay)",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "DATAGREX",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "DATA4 Paris Marcoussis PAR2",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Cogent Paris",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "NeoCenter Paris",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "nLighten Paris PAR1",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "AtlasEdge DC Paris CDG001",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "SI Cloud Montpellier",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "EXA Edge DC Bordeaux",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "System-Net HDC 1",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "ETIX Vendée #1",
    "ColocatedASes": 2
  },
  {
    "DataCenter": "Groupe Cyllene - DC - Nanterre",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Alpes Networks DataCenter",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "MEDIACTIVE MN3",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Eurofiber DC - AUC00",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "RTDC",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "dc2scale ALP1 (Grenoble)",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Orange / Chartres",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "EXA Edge DC Poitiers",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Viatel Amiens",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Extendo Datacenter Belfort",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Hexatom Sophia Antipolis",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Celeste Fil d’Ariane",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "IzarHost",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "NetaPOP Pontarlier",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Ikoula IKDC2",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Groupe Cyllene - DC - Montigny les Bretonneux",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Digital Realty Paris PAR12",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Fiducial Cloud LYO1",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "NETICENTER",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "COLT DC Paris SouthWest",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "OT - Capella",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "EXA Edge DC Marseille",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "OT - Armor",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "NetaPOP Besançon",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Multicoms Paris (Velizy)",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "COLT DC Paris III",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "BT-BLUE Datacenter 1",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Dataxion France DTX01",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "OPCORE - DC4 / PAR4",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Castle-IT Tours",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Neuf Rouen",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Neuf Reims",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Thésée Datacenter",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Sanef Telecom Reims",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Ultraedge Canteleu",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "Groupe Cyllene - DC - Courbevoie",
    "ColocatedASes": 1
  },
  {
    "DataCenter": "BB1",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "ICODIA NETWORK INTEGRITY",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "UltraEdge Velizy",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Cloudata",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "MENGINE",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Centrinuity Toulouse",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Strasbourg",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "HELIANTIS",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Alionis VBO",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "DTiX Chalon-sur-Saône",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Alliance Réseaux",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "nLighten Sophia Antipolis NCE2",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Magic OnLine",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "RUBIX DATACENTER - DC-1",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "VirtuaCenter Auxerre",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Serinya Telecom",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Vauchelles",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "dc2scale Nanterre",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "nLighten Paris PAR3",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "REDHEBERG SAS",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Metroptics Datacenter",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "connect-ix",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Ouiherberg Aimargues",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Nancy",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Ychoux",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Civicos Networking DCROUBAIX",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Betech Solution",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Crypteo Marssac",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "dc2scale LIL1 (Lille Datacenter)",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Sequedin",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "dc2scale MRS1 (Marseille datacenter)",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Reliance Plerin",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "PHOCEA DC-M1",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Neuf Caen",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Smartdc Paris",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Digital Realty Paris PAR13",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "ATE #1",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "SynAApS",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "DARVA Hosting",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "PAM00",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Sigma DC3",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "OT - Rezé",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Reliance St. Denis",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Association Alsace Reseau Neutre",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Toulouse",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "IMADIFF",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Sipartech Paris",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "ADISTA Groupe",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "EXA Edge DC Willerval",
    "ColocatedASes": 0
  },
  {
    "DataCenter": "Firstheberg",
    "ColocatedASes": 0
  }
]
```
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

> **Output (110 record(s)):**

```json
[
  {
    "Operator": "Cogent Communications, Inc.",
    "DataCenterCount": 16
  },
  {
    "Operator": "UltraEdge",
    "DataCenterCount": 12
  },
  {
    "Operator": "Etix Everywhere",
    "DataCenterCount": 12
  },
  {
    "Operator": "Digital Realty",
    "DataCenterCount": 11
  },
  {
    "Operator": "EXA Infrastructure",
    "DataCenterCount": 11
  },
  {
    "Operator": "Equinix, Inc.",
    "DataCenterCount": 9
  },
  {
    "Operator": "nLighten HQ BV",
    "DataCenterCount": 8
  },
  {
    "Operator": "dc2scale SAS",
    "DataCenterCount": 8
  },
  {
    "Operator": "TDF",
    "DataCenterCount": 5
  },
  {
    "Operator": "Eurofiber France",
    "DataCenterCount": 5
  },
  {
    "Operator": "Colt Technology Services Group",
    "DataCenterCount": 4
  },
  {
    "Operator": "OPCORE",
    "DataCenterCount": 4
  },
  {
    "Operator": "Neuf Cegetel SA.",
    "DataCenterCount": 4
  },
  {
    "Operator": "Groupe Oceanet Technology",
    "DataCenterCount": 4
  },
  {
    "Operator": "Telehouse - Global Data Centers",
    "DataCenterCount": 3
  },
  {
    "Operator": "Cyllene SAS",
    "DataCenterCount": 3
  },
  {
    "Operator": "Free Pro",
    "DataCenterCount": 3
  },
  {
    "Operator": "Sipartech SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "Zayo Group",
    "DataCenterCount": 2
  },
  {
    "Operator": "DTiX SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "DATA4 s.a r.l",
    "DataCenterCount": 2
  },
  {
    "Operator": "Hexanet SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "Celeste SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "Netalis SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "Ikoula Net SAS",
    "DataCenterCount": 2
  },
  {
    "Operator": "WEBINDUSTRIE",
    "DataCenterCount": 2
  },
  {
    "Operator": "FLAG Telecom",
    "DataCenterCount": 2
  },
  {
    "Operator": "Alpes Networks SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "MEDIACTIVE GROUP",
    "DataCenterCount": 1
  },
  {
    "Operator": "ICODIA",
    "DataCenterCount": 1
  },
  {
    "Operator": "ABICOM SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Adeli",
    "DataCenterCount": 1
  },
  {
    "Operator": "ResoLv SARL",
    "DataCenterCount": 1
  },
  {
    "Operator": "Cloudata",
    "DataCenterCount": 1
  },
  {
    "Operator": "IELO-LIAZO SERVICES SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Penta C.V.",
    "DataCenterCount": 1
  },
  {
    "Operator": "Orange S.A.",
    "DataCenterCount": 1
  },
  {
    "Operator": "MENGINE",
    "DataCenterCount": 1
  },
  {
    "Operator": "Centrinuity Toulouse",
    "DataCenterCount": 1
  },
  {
    "Operator": "Verizon Communications, Inc.",
    "DataCenterCount": 1
  },
  {
    "Operator": "HELIANTIS SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Alionis",
    "DataCenterCount": 1
  },
  {
    "Operator": "PROSOLUCE SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Global Switch",
    "DataCenterCount": 1
  },
  {
    "Operator": "★ Dyjix SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Alliance Reseaux SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Treefaz",
    "DataCenterCount": 1
  },
  {
    "Operator": "Somme-numerique DC1",
    "DataCenterCount": 1
  },
  {
    "Operator": "Orange / Val de Rueil",
    "DataCenterCount": 1
  },
  {
    "Operator": "Magic OnLine",
    "DataCenterCount": 1
  },
  {
    "Operator": "Xavier Lafaure",
    "DataCenterCount": 1
  },
  {
    "Operator": "Completel SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Datacampus SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "RUBIX DATACENTER",
    "DataCenterCount": 1
  },
  {
    "Operator": "Ad Valem Technologies",
    "DataCenterCount": 1
  },
  {
    "Operator": "Viatel Amiens",
    "DataCenterCount": 1
  },
  {
    "Operator": "Advanced MedioMatrix",
    "DataCenterCount": 1
  },
  {
    "Operator": "Virtua Networks",
    "DataCenterCount": 1
  },
  {
    "Operator": "Extendo Datacenter",
    "DataCenterCount": 1
  },
  {
    "Operator": "Serinya Telecom",
    "DataCenterCount": 1
  },
  {
    "Operator": "Hexatom S.A.R.L.",
    "DataCenterCount": 1
  },
  {
    "Operator": "Orange Business - La Fabrique",
    "DataCenterCount": 1
  },
  {
    "Operator": "IZARLINK SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "moji",
    "DataCenterCount": 1
  },
  {
    "Operator": "Quantic Telecom SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Techcrea",
    "DataCenterCount": 1
  },
  {
    "Operator": "Montpellier Internet Telecom Datacenter",
    "DataCenterCount": 1
  },
  {
    "Operator": "TelcoCenter",
    "DataCenterCount": 1
  },
  {
    "Operator": "LASOTEL SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "TAS France",
    "DataCenterCount": 1
  },
  {
    "Operator": "XSALTO",
    "DataCenterCount": 1
  },
  {
    "Operator": "NEXEREN",
    "DataCenterCount": 1
  },
  {
    "Operator": "REDHEBERG SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Metroptics",
    "DataCenterCount": 1
  },
  {
    "Operator": "SAS CONNECT-IX",
    "DataCenterCount": 1
  },
  {
    "Operator": "OuiHeberg SARL",
    "DataCenterCount": 1
  },
  {
    "Operator": "Fiducial Cloud Organisation",
    "DataCenterCount": 1
  },
  {
    "Operator": "Axione Lotim Telecom",
    "DataCenterCount": 1
  },
  {
    "Operator": "Civicos Networking, S.L.U.",
    "DataCenterCount": 1
  },
  {
    "Operator": "DATAGREX SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "BeTech Solution",
    "DataCenterCount": 1
  },
  {
    "Operator": "AZA TELECOM SARL",
    "DataCenterCount": 1
  },
  {
    "Operator": "GREEN DATA SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Comarch SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "PHOCEA DC",
    "DataCenterCount": 1
  },
  {
    "Operator": "Axione Adtim",
    "DataCenterCount": 1
  },
  {
    "Operator": "Smartdc",
    "DataCenterCount": 1
  },
  {
    "Operator": "AtlasEdge",
    "DataCenterCount": 1
  },
  {
    "Operator": "ATE - Avenir Télématique",
    "DataCenterCount": 1
  },
  {
    "Operator": "MULTICOMS FACILITIES MANAGEMENT",
    "DataCenterCount": 1
  },
  {
    "Operator": "Centre de Calcul de l'Institut National de Physique NuclÃ©aire et de Physique des Particules",
    "DataCenterCount": 1
  },
  {
    "Operator": "Bretagne Telecom",
    "DataCenterCount": 1
  },
  {
    "Operator": "SynAAps",
    "DataCenterCount": 1
  },
  {
    "Operator": "DEVELOPPEMENT D'APPLICATIONS SUR RESEAUX A VALEUR AJOUTEE SA",
    "DataCenterCount": 1
  },
  {
    "Operator": "ITinSell Cloud",
    "DataCenterCount": 1
  },
  {
    "Operator": "SI Cloud SASU",
    "DataCenterCount": 1
  },
  {
    "Operator": "EQUADEX SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "SIGMA INFORMATIQUE SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Département de la Haute-Saône",
    "DataCenterCount": 1
  },
  {
    "Operator": "EASYTEAM (ex DATAXION)",
    "DataCenterCount": 1
  },
  {
    "Operator": "Caste-IT SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "Association Alsace Reseau Neutre",
    "DataCenterCount": 1
  },
  {
    "Operator": "Axione Limousin",
    "DataCenterCount": 1
  },
  {
    "Operator": "System-Net SAS",
    "DataCenterCount": 1
  },
  {
    "Operator": "IMA'DIFF",
    "DataCenterCount": 1
  },
  {
    "Operator": "Aqua Ray",
    "DataCenterCount": 1
  },
  {
    "Operator": "Thésée Datacenter",
    "DataCenterCount": 1
  },
  {
    "Operator": "Sanef Telecom",
    "DataCenterCount": 1
  },
  {
    "Operator": "Firstheberg",
    "DataCenterCount": 1
  },
  {
    "Operator": "D-LAKE SAS",
    "DataCenterCount": 1
  }
]
```
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

> **Output (20 record(s)):**

```json
[
  {
    "ASN": 29066,
    "NetworkName": "VELIANET-AS",
    "PrefixCount": 435
  },
  {
    "ASN": 62610,
    "NetworkName": "ZEN-DPS",
    "PrefixCount": 288
  },
  {
    "ASN": 8677,
    "NetworkName": "WORLDLINE",
    "PrefixCount": 200
  },
  {
    "ASN": 12696,
    "NetworkName": "AXA Technology Services France GIE",
    "PrefixCount": 115
  },
  {
    "ASN": 2060,
    "NetworkName": "FR-RENATER",
    "PrefixCount": 91
  },
  {
    "ASN": 207147,
    "NetworkName": "NETCOM-AS",
    "PrefixCount": 82
  },
  {
    "ASN": 34949,
    "NetworkName": "IDLINE SAS",
    "PrefixCount": 69
  },
  {
    "ASN": 60855,
    "NetworkName": "DISIC-RIE-AS",
    "PrefixCount": 65
  },
  {
    "ASN": 210403,
    "NetworkName": "Groupe LWS SARL",
    "PrefixCount": 56
  },
  {
    "ASN": 25215,
    "NetworkName": "BNP PARIBAS S.A.",
    "PrefixCount": 55
  },
  {
    "ASN": 206178,
    "NetworkName": "AWEBO",
    "PrefixCount": 50
  },
  {
    "ASN": 205710,
    "NetworkName": "Association CREALAB",
    "PrefixCount": 50
  },
  {
    "ASN": 200546,
    "NetworkName": "ALEXANDRE-SAGE-TRADING-AS-VELYS-SOFTWARE Alexandre SAGE trading as VELYS SOFTWARE",
    "PrefixCount": 50
  },
  {
    "ASN": 206445,
    "NetworkName": "LE RESEAU VERT",
    "PrefixCount": 50
  },
  {
    "ASN": 207480,
    "NetworkName": "ALGOMEDIA",
    "PrefixCount": 50
  },
  {
    "ASN": 211980,
    "NetworkName": "Association ECHOES",
    "PrefixCount": 50
  },
  {
    "ASN": 207001,
    "NetworkName": "Association LOS AMIGOS",
    "PrefixCount": 50
  },
  {
    "ASN": 206809,
    "NetworkName": "PRO RESEAU",
    "PrefixCount": 48
  },
  {
    "ASN": 206778,
    "NetworkName": "OPTA",
    "PrefixCount": 48
  },
  {
    "ASN": 215727,
    "NetworkName": "ASNSWORLDWIDE",
    "PrefixCount": 47
  }
]
```
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

> **Output (23 record(s)):**

```json
[
  {
    "IXP": "France-IX Paris",
    "LocalMembers": 235,
    "ForeignMembers": 212
  },
  {
    "IXP": "Equinix Paris",
    "LocalMembers": 151,
    "ForeignMembers": 92
  },
  {
    "IXP": "France-IX AURA",
    "LocalMembers": 59,
    "ForeignMembers": 15
  },
  {
    "IXP": "nine",
    "LocalMembers": 48,
    "ForeignMembers": 31
  },
  {
    "IXP": "France-IX Marseille",
    "LocalMembers": 37,
    "ForeignMembers": 75
  },
  {
    "IXP": "Lillix",
    "LocalMembers": 32,
    "ForeignMembers": 8
  },
  {
    "IXP": "Hopus",
    "LocalMembers": 27,
    "ForeignMembers": 6
  },
  {
    "IXP": "SFINX",
    "LocalMembers": 19,
    "ForeignMembers": 5
  },
  {
    "IXP": "BreizhIX",
    "LocalMembers": 18,
    "ForeignMembers": 2
  },
  {
    "IXP": "AuvernIX",
    "LocalMembers": 12,
    "ForeignMembers": 1
  },
  {
    "IXP": "EuroRhine-IX",
    "LocalMembers": 10,
    "ForeignMembers": 1
  },
  {
    "IXP": "DE-CIX Marseille",
    "LocalMembers": 10,
    "ForeignMembers": 112
  },
  {
    "IXP": "France-IX Lille",
    "LocalMembers": 10,
    "ForeignMembers": 6
  },
  {
    "IXP": "BGP.Exchange - Paris",
    "LocalMembers": 10,
    "ForeignMembers": 34
  },
  {
    "IXP": "Ouest.Network",
    "LocalMembers": 9,
    "ForeignMembers": 0
  },
  {
    "IXP": "France-IX Toulouse",
    "LocalMembers": 9,
    "ForeignMembers": 4
  },
  {
    "IXP": "B�arnIX",
    "LocalMembers": 8,
    "ForeignMembers": 1
  },
  {
    "IXP": "BGP.Exchange - Lyon",
    "LocalMembers": 8,
    "ForeignMembers": 16
  },
  {
    "IXP": "SBG-IX",
    "LocalMembers": 3,
    "ForeignMembers": 2
  },
  {
    "IXP": "BrestIX",
    "LocalMembers": 2,
    "ForeignMembers": 0
  },
  {
    "IXP": "MPLIX",
    "LocalMembers": 2,
    "ForeignMembers": 0
  },
  {
    "IXP": "NormandIX",
    "LocalMembers": 1,
    "ForeignMembers": 0
  },
  {
    "IXP": "France-IX Bordeaux",
    "LocalMembers": 1,
    "ForeignMembers": 1
  }
]
```

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

> **Output (15 record(s)):**

```json
[
  {
    "ASN": 6939,
    "NetworkName": "HURRICANE",
    "IXPs": [
      "Equinix Paris",
      "France-IX Marseille",
      "nine",
      "DE-CIX Marseille",
      "France-IX AURA",
      "France-IX Paris"
    ],
    "CaidaRank": 7
  },
  {
    "ASN": 6461,
    "NetworkName": "ZAYO-6461",
    "IXPs": [
      "Equinix Paris",
      "Lillix",
      "France-IX Marseille",
      "nine",
      "France-IX AURA",
      "France-IX Paris"
    ],
    "CaidaRank": 8
  },
  {
    "ASN": 9002,
    "NetworkName": "RETN",
    "IXPs": [
      "France-IX Paris"
    ],
    "CaidaRank": 11
  },
  {
    "ASN": 12956,
    "NetworkName": "TELXIUS",
    "IXPs": [
      "DE-CIX Marseille"
    ],
    "CaidaRank": 13
  },
  {
    "ASN": 1273,
    "NetworkName": "CW",
    "IXPs": [
      "Equinix Paris"
    ],
    "CaidaRank": 14
  },
  {
    "ASN": 4637,
    "NetworkName": "ASN-TELSTRA-GLOBAL",
    "IXPs": [
      "France-IX Paris"
    ],
    "CaidaRank": 16
  },
  {
    "ASN": 37468,
    "NetworkName": "ANGOLA-CABLES",
    "IXPs": [
      "France-IX Marseille"
    ],
    "CaidaRank": 21
  },
  {
    "ASN": 9498,
    "NetworkName": "BBIL-AP",
    "IXPs": [
      "DE-CIX Marseille"
    ],
    "CaidaRank": 22
  },
  {
    "ASN": 58453,
    "NetworkName": "CMI-INT-HK",
    "IXPs": [
      "Equinix Paris",
      "France-IX Paris"
    ],
    "CaidaRank": 26
  },
  {
    "ASN": 20485,
    "NetworkName": "TRANSTELECOM",
    "IXPs": [
      "France-IX Paris"
    ],
    "CaidaRank": 27
  },
  {
    "ASN": 31133,
    "NetworkName": "MF-MGSM-AS",
    "IXPs": [
      "DE-CIX Marseille"
    ],
    "CaidaRank": 28
  },
  {
    "ASN": 20764,
    "NetworkName": "CJSC RASCOM",
    "IXPs": [
      "France-IX Paris"
    ],
    "CaidaRank": 29
  },
  {
    "ASN": 33891,
    "NetworkName": "CORE-BACKBONE",
    "IXPs": [
      "France-IX Paris"
    ],
    "CaidaRank": 37
  },
  {
    "ASN": 15412,
    "NetworkName": "FLAG Telecom",
    "IXPs": [
      "Equinix Paris",
      "France-IX Marseille",
      "France-IX Paris"
    ],
    "CaidaRank": 43
  },
  {
    "ASN": 8220,
    "NetworkName": "COLT",
    "IXPs": [
      "Equinix Paris",
      "France-IX Marseille",
      "France-IX Paris"
    ],
    "CaidaRank": 44
  }
]
```

---

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "GeoCoveragePoints": 1016,
    "ActiveOperators": 1524
  }
]
```

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

> **Output (20 record(s)):**

```json
[
  {
    "ASN": 12322,
    "OperatorName": "Free FR",
    "AnnouncedPrefixes": 1065,
    "FacilityPresence": 14
  },
  {
    "ASN": 3215,
    "OperatorName": "AS3215",
    "AnnouncedPrefixes": 984,
    "FacilityPresence": 6
  },
  {
    "ASN": 16276,
    "OperatorName": "OVH",
    "AnnouncedPrefixes": 792,
    "FacilityPresence": 5
  },
  {
    "ASN": 5511,
    "OperatorName": "OPENTRANSIT",
    "AnnouncedPrefixes": 576,
    "FacilityPresence": 21
  },
  {
    "ASN": 51167,
    "OperatorName": "CONTABO",
    "AnnouncedPrefixes": 570,
    "FacilityPresence": 0
  },
  {
    "ASN": 29066,
    "OperatorName": "VELIANET-AS",
    "AnnouncedPrefixes": 435,
    "FacilityPresence": 0
  },
  {
    "ASN": 2200,
    "OperatorName": "FR-RENATER",
    "AnnouncedPrefixes": 356,
    "FacilityPresence": 4
  },
  {
    "ASN": 63023,
    "OperatorName": "AS-GLOBALTELEHOST",
    "AnnouncedPrefixes": 323,
    "FacilityPresence": 2
  },
  {
    "ASN": 62610,
    "OperatorName": "ZEN-DPS",
    "AnnouncedPrefixes": 288,
    "FacilityPresence": 0
  },
  {
    "ASN": 46475,
    "OperatorName": "LIMESTONENETWORKS",
    "AnnouncedPrefixes": 262,
    "FacilityPresence": 1
  },
  {
    "ASN": 25369,
    "OperatorName": "BANDWIDTH-AS",
    "AnnouncedPrefixes": 207,
    "FacilityPresence": 1
  },
  {
    "ASN": 8677,
    "OperatorName": "WORLDLINE",
    "AnnouncedPrefixes": 200,
    "FacilityPresence": 0
  },
  {
    "ASN": 16347,
    "OperatorName": "ADISTA SAS",
    "AnnouncedPrefixes": 165,
    "FacilityPresence": 21
  },
  {
    "ASN": 15557,
    "OperatorName": "LDCOMNET",
    "AnnouncedPrefixes": 158,
    "FacilityPresence": 6
  },
  {
    "ASN": 1299,
    "OperatorName": "Arelion",
    "AnnouncedPrefixes": 139,
    "FacilityPresence": 14
  },
  {
    "ASN": 43350,
    "OperatorName": "NFORCE",
    "AnnouncedPrefixes": 130,
    "FacilityPresence": 0
  },
  {
    "ASN": 12696,
    "OperatorName": "AXA Technology Services France GIE",
    "AnnouncedPrefixes": 115,
    "FacilityPresence": 0
  },
  {
    "ASN": 34177,
    "OperatorName": "CELESTE",
    "AnnouncedPrefixes": 101,
    "FacilityPresence": 33
  },
  {
    "ASN": 2060,
    "OperatorName": "FR-RENATER",
    "AnnouncedPrefixes": 91,
    "FacilityPresence": 0
  },
  {
    "ASN": 25540,
    "OperatorName": "ALPHALINK-AS",
    "AnnouncedPrefixes": 91,
    "FacilityPresence": 5
  }
]
```

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

> **Output (20 record(s)):**

```json
[
  {
    "ASN": 29075,
    "OperatorName": "IELO",
    "NumberOfFacilities": 68
  },
  {
    "ASN": 35625,
    "OperatorName": "EUROFIBER-FRANCE",
    "NumberOfFacilities": 52
  },
  {
    "ASN": 30781,
    "OperatorName": "Free Pro",
    "NumberOfFacilities": 42
  },
  {
    "ASN": 8309,
    "OperatorName": "SIPARTECH",
    "NumberOfFacilities": 41
  },
  {
    "ASN": 8218,
    "OperatorName": "NEO-ASN",
    "NumberOfFacilities": 34
  },
  {
    "ASN": 34177,
    "OperatorName": "CELESTE",
    "NumberOfFacilities": 33
  },
  {
    "ASN": 200780,
    "OperatorName": "APPLIWAVE",
    "NumberOfFacilities": 27
  },
  {
    "ASN": 39180,
    "OperatorName": "LASOTEL",
    "NumberOfFacilities": 25
  },
  {
    "ASN": 8487,
    "OperatorName": "PHIBEE",
    "NumberOfFacilities": 23
  },
  {
    "ASN": 62000,
    "OperatorName": "NETRIX-AS",
    "NumberOfFacilities": 23
  },
  {
    "ASN": 206120,
    "OperatorName": "KOESIO Networks SAS",
    "NumberOfFacilities": 22
  },
  {
    "ASN": 212815,
    "OperatorName": "AS-DYJIX",
    "NumberOfFacilities": 22
  },
  {
    "ASN": 16347,
    "OperatorName": "ADISTA SAS",
    "NumberOfFacilities": 21
  },
  {
    "ASN": 5511,
    "OperatorName": "OPENTRANSIT",
    "NumberOfFacilities": 21
  },
  {
    "ASN": 43646,
    "OperatorName": "TDF",
    "NumberOfFacilities": 20
  },
  {
    "ASN": 30889,
    "OperatorName": "ADISTA SAS",
    "NumberOfFacilities": 20
  },
  {
    "ASN": 34019,
    "OperatorName": "HIVANE",
    "NumberOfFacilities": 18
  },
  {
    "ASN": 47160,
    "OperatorName": "MOJI",
    "NumberOfFacilities": 16
  },
  {
    "ASN": 20565,
    "OperatorName": "NETALIS",
    "NumberOfFacilities": 16
  },
  {
    "ASN": 44407,
    "OperatorName": "ASN-LINKT",
    "NumberOfFacilities": 15
  }
]
```

---

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "TotalASes": 2238,
    "ActiveASes": 1524,
    "DormantASes": 714,
    "ActivePercent": 68.1
  }
]
```

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "DomesticFacilities": 168,
    "InternationalFacilities": 453,
    "TotalFacilities": 621
  }
]
```

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "IXPConnected": 346,
    "NotIXPConnected": 1178,
    "TotalActive": 1524,
    "IXPAdoptionPercent": 22.7
  }
]
```

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "DomesticPeers": 1271,
    "InternationalPeers": 10613,
    "TotalPeers": 11884
  }
]
```

---

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

> **Output (1 record(s)):**

```json
[
  {
    "Country": "France",
    "Originated_Prefixes": 15996,
    "IPv4_Prefixes": 13138,
    "IPv6_Prefixes": 2858,
    "ActiveOperators": 1524,
    "IPv6_SharePercent": 17.87
  }
]
```

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

> **Output (20 record(s)):**

```json
[
  {
    "ASN": 12322,
    "OperatorName": "Free FR",
    "TotalPrefixes": 1065,
    "IPv4Prefixes": 538,
    "IPv6Prefixes": 527,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 3215,
    "OperatorName": "AS3215",
    "TotalPrefixes": 984,
    "IPv4Prefixes": 941,
    "IPv6Prefixes": 43,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 16276,
    "OperatorName": "OVH",
    "TotalPrefixes": 792,
    "IPv4Prefixes": 751,
    "IPv6Prefixes": 41,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 5511,
    "OperatorName": "OPENTRANSIT",
    "TotalPrefixes": 576,
    "IPv4Prefixes": 563,
    "IPv6Prefixes": 13,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 51167,
    "OperatorName": "CONTABO",
    "TotalPrefixes": 570,
    "IPv4Prefixes": 565,
    "IPv6Prefixes": 5,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 29066,
    "OperatorName": "VELIANET-AS",
    "TotalPrefixes": 435,
    "IPv4Prefixes": 425,
    "IPv6Prefixes": 10,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 2200,
    "OperatorName": "FR-RENATER",
    "TotalPrefixes": 356,
    "IPv4Prefixes": 354,
    "IPv6Prefixes": 2,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 63023,
    "OperatorName": "AS-GLOBALTELEHOST",
    "TotalPrefixes": 323,
    "IPv4Prefixes": 298,
    "IPv6Prefixes": 25,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 62610,
    "OperatorName": "ZEN-DPS",
    "TotalPrefixes": 288,
    "IPv4Prefixes": 209,
    "IPv6Prefixes": 79,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 46475,
    "OperatorName": "LIMESTONENETWORKS",
    "TotalPrefixes": 262,
    "IPv4Prefixes": 238,
    "IPv6Prefixes": 24,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 25369,
    "OperatorName": "BANDWIDTH-AS",
    "TotalPrefixes": 207,
    "IPv4Prefixes": 188,
    "IPv6Prefixes": 19,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 8677,
    "OperatorName": "WORLDLINE",
    "TotalPrefixes": 200,
    "IPv4Prefixes": 200,
    "IPv6Prefixes": 0,
    "IPv6Adopted": "No"
  },
  {
    "ASN": 16347,
    "OperatorName": "ADISTA SAS",
    "TotalPrefixes": 165,
    "IPv4Prefixes": 147,
    "IPv6Prefixes": 18,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 15557,
    "OperatorName": "LDCOMNET",
    "TotalPrefixes": 158,
    "IPv4Prefixes": 146,
    "IPv6Prefixes": 12,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 1299,
    "OperatorName": "Arelion",
    "TotalPrefixes": 139,
    "IPv4Prefixes": 115,
    "IPv6Prefixes": 24,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 43350,
    "OperatorName": "NFORCE",
    "TotalPrefixes": 130,
    "IPv4Prefixes": 109,
    "IPv6Prefixes": 21,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 12696,
    "OperatorName": "AXA Technology Services France GIE",
    "TotalPrefixes": 115,
    "IPv4Prefixes": 115,
    "IPv6Prefixes": 0,
    "IPv6Adopted": "No"
  },
  {
    "ASN": 34177,
    "OperatorName": "CELESTE",
    "TotalPrefixes": 101,
    "IPv4Prefixes": 90,
    "IPv6Prefixes": 11,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 25540,
    "OperatorName": "ALPHALINK-AS",
    "TotalPrefixes": 91,
    "IPv4Prefixes": 84,
    "IPv6Prefixes": 7,
    "IPv6Adopted": "Yes"
  },
  {
    "ASN": 2060,
    "OperatorName": "FR-RENATER",
    "TotalPrefixes": 91,
    "IPv4Prefixes": 91,
    "IPv6Prefixes": 0,
    "IPv6Adopted": "No"
  }
]
```

---

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

> **Output (30 record(s)):**

```json
[
  {
    "asn": 3215,
    "asName": "AS3215 Orange S.A.",
    "marketSharePercent": 35.38051167179335
  },
  {
    "asn": 12322,
    "asName": "PROXAD Free SAS",
    "marketSharePercent": 18.649609448176673
  },
  {
    "asn": 5410,
    "asName": "BOUYGTEL-ISP Bouygues Telecom SA",
    "marketSharePercent": 17.747870947714453
  },
  {
    "asn": 15557,
    "asName": "LDCOMNET Societe Francaise Du Radiotelephone - SFR SA",
    "marketSharePercent": 17.522857472432
  },
  {
    "asn": 51207,
    "asName": "FREEM Free Mobile SAS",
    "marketSharePercent": 4.545856517745062
  },
  {
    "asn": 16276,
    "asName": "OVH OVH SAS",
    "marketSharePercent": 0.8547753793962675
  },
  {
    "asn": 63023,
    "asName": "AS-GLOBALTELEHOST - GTHost",
    "marketSharePercent": 0.7778947419995292
  },
  {
    "asn": 12876,
    "asName": "AS12876 Scaleway SAS",
    "marketSharePercent": 0.6916868077604803
  },
  {
    "asn": 51167,
    "asName": "CONTABO Contabo GmbH",
    "marketSharePercent": 0.323644195442315
  },
  {
    "asn": 31404,
    "asName": "Lycatel-AS LYCATEL DISTRIBUTION UK LIMITED",
    "marketSharePercent": 0.2571962786868061
  },
  {
    "asn": 13335,
    "asName": "CLOUDFLARENET - Cloudflare, Inc.",
    "marketSharePercent": 0.21004564387110403
  },
  {
    "asn": 30058,
    "asName": "FDCSERVERS - FDCservers.net",
    "marketSharePercent": 0.20984300804476327
  },
  {
    "asn": 14593,
    "asName": "SPACEX-STARLINK - Space Exploration Technologies Corporation",
    "marketSharePercent": 0.1865474490538752
  },
  {
    "asn": 21859,
    "asName": "ZEN-ECN",
    "marketSharePercent": 0.1690633040975202
  },
  {
    "asn": 29066,
    "asName": "VELIANET-AS velia.net Internetdienste GmbH",
    "marketSharePercent": 0.1433618227207507
  },
  {
    "asn": 16509,
    "asName": "AMAZON-02 - Amazon.com, Inc.",
    "marketSharePercent": 0.13970076797768416
  },
  {
    "asn": 52075,
    "asName": "WIFIRST Wifirst S.A.S.",
    "marketSharePercent": 0.12223628172089958
  },
  {
    "asn": 62610,
    "asName": "ZEN-DPS - Zenlayer Inc",
    "marketSharePercent": 0.10571087642051495
  },
  {
    "asn": 212238,
    "asName": "CDNEXT Datacamp Limited",
    "marketSharePercent": 0.0926227191296265
  },
  {
    "asn": 136787,
    "asName": "PACKETHUBSA-AS-AP PacketHub S.A.",
    "marketSharePercent": 0.09188173737658949
  },
  {
    "asn": 2200,
    "asName": "FR-RENATER Reseau National de telecommunications pour la Technologie",
    "marketSharePercent": 0.09037104192498954
  },
  {
    "asn": 199636,
    "asName": "FREEBOXPRO Free Pro SAS",
    "marketSharePercent": 0.08000788283608619
  },
  {
    "asn": 42487,
    "asName": "Vialis-Moselle Vialis SEM",
    "marketSharePercent": 0.07747795942214553
  },
  {
    "asn": 63949,
    "asName": "AKAMAI-LINODE-AP Akamai Connected Cloud",
    "marketSharePercent": 0.0765600493729752
  },
  {
    "asn": 16347,
    "asName": "INHERENT ADISTA SAS",
    "marketSharePercent": 0.0656237635812126
  },
  {
    "asn": 8362,
    "asName": "NordNet SA",
    "marketSharePercent": 0.06443063173805709
  },
  {
    "asn": 41114,
    "asName": "ORNETHD ORNE THD SPL",
    "marketSharePercent": 0.05723554769530177
  },
  {
    "asn": 8399,
    "asName": "SEWAN-FR SEWAN SAS",
    "marketSharePercent": 0.052243750212087124
  },
  {
    "asn": 12727,
    "asName": "VIALIS Vialis SEM",
    "marketSharePercent": 0.04772073710324283
  },
  {
    "asn": 174,
    "asName": "COGENT-174 - Cogent Communications, LLC",
    "marketSharePercent": 0.04717483013825026
  }
]
```
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

> **Output (1 record(s)):**

```json
[
  {
    "hhi": 2244.5674407387573,
    "totalAS": 65,
    "marketConcentration": "Moderately Concentrated Market"
  }
]
```

---

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

> **Output (10 record(s)):**

```json
[
  {
    "providerASN": 12654,
    "providerName": "RIPE-NCC-RIS-AS Reseaux IP Europeens Network Coordination Centre (RIPE NCC)",
    "localCustomers": 7
  },
  {
    "providerASN": 4455,
    "providerName": "BSO IX Reach Ltd",
    "localCustomers": 4
  },
  {
    "providerASN": 9009,
    "providerName": "M247 M247 Europe SRL",
    "localCustomers": 3
  },
  {
    "providerASN": 200019,
    "providerName": "AlexHost ALEXHOST SRL",
    "localCustomers": 3
  },
  {
    "providerASN": 55256,
    "providerName": "NETSKOPE - Netskope Inc",
    "localCustomers": 3
  },
  {
    "providerASN": 20776,
    "providerName": "OUTREMER-AS Outremer Telecom SAS",
    "localCustomers": 3
  },
  {
    "providerASN": 52025,
    "providerName": "PARADOXNETWORKS-LIMITED ParadoxNetworks Limited",
    "localCustomers": 3
  },
  {
    "providerASN": 25091,
    "providerName": "IP-Max IP-Max SA",
    "localCustomers": 3
  },
  {
    "providerASN": 3573,
    "providerName": "ACCENTURE - Accenture LLP",
    "localCustomers": 3
  },
  {
    "providerASN": 21859,
    "providerName": "ZEN-ECN",
    "localCustomers": 3
  }
]
```

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

> **Output (50 record(s)):**

```json
[
  {
    "providerASN": 6939,
    "providerName": "HURRICANE - Hurricane Electric LLC",
    "averageHegemony": 0.3616924934522763,
    "dependentASNs": 762
  },
  {
    "providerASN": 174,
    "providerName": "COGENT-174 - Cogent Communications, LLC",
    "averageHegemony": 0.45982608872302655,
    "dependentASNs": 410
  },
  {
    "providerASN": 3356,
    "providerName": "LEVEL3 - Level 3 Parent, LLC",
    "averageHegemony": 0.32980246239887173,
    "dependentASNs": 161
  },
  {
    "providerASN": 6762,
    "providerName": "SEABONE-NET TELECOM ITALIA SPARKLE S.p.A.",
    "averageHegemony": 0.2839998442887947,
    "dependentASNs": 131
  },
  {
    "providerASN": 6461,
    "providerName": "ZAYO-6461 - Zayo Bandwidth",
    "averageHegemony": 0.4446795464390604,
    "dependentASNs": 105
  },
  {
    "providerASN": 8220,
    "providerName": "COLT COLT Technology Services Group Limited",
    "averageHegemony": 0.6860529475859558,
    "dependentASNs": 99
  },
  {
    "providerASN": 137409,
    "providerName": "GSLNETWORKS-AS-AP GSL Networks Pty LTD",
    "averageHegemony": 0.3443724997198507,
    "dependentASNs": 91
  },
  {
    "providerASN": 3257,
    "providerName": "GTT-BACKBONE GTT Communications Inc.",
    "averageHegemony": 0.4401493959727144,
    "dependentASNs": 60
  },
  {
    "providerASN": 29222,
    "providerName": "Infomaniak-AS Infomaniak Network SA",
    "averageHegemony": 0.12451615605026818,
    "dependentASNs": 56
  },
  {
    "providerASN": 2914,
    "providerName": "NTT-DATA-2914 - NTT America, Inc.",
    "averageHegemony": 0.24954843032761384,
    "dependentASNs": 48
  },
  {
    "providerASN": 9002,
    "providerName": "RETN-AS RETN Limited",
    "averageHegemony": 0.24807248910509788,
    "dependentASNs": 40
  },
  {
    "providerASN": 21320,
    "providerName": "GEANT_IAS_VRF GEANT Vereniging",
    "averageHegemony": 0.15633080341877825,
    "dependentASNs": 37
  },
  {
    "providerASN": 25091,
    "providerName": "IP-Max IP-Max SA",
    "averageHegemony": 0.5982164423444529,
    "dependentASNs": 28
  },
  {
    "providerASN": 1273,
    "providerName": "CW Vodafone Group PLC",
    "averageHegemony": 0.14575581395348838,
    "dependentASNs": 27
  },
  {
    "providerASN": 20473,
    "providerName": "AS-VULTR - The Constant Company, LLC",
    "averageHegemony": 0.7801846590909093,
    "dependentASNs": 25
  },
  {
    "providerASN": 199524,
    "providerName": "GCORE G-Core Labs S.A.",
    "averageHegemony": 0.6655303030303031,
    "dependentASNs": 18
  },
  {
    "providerASN": 4455,
    "providerName": "BSO IX Reach Ltd",
    "averageHegemony": 0.539139293139293,
    "dependentASNs": 18
  },
  {
    "providerASN": 15830,
    "providerName": "Equinix Equinix (EMEA) Acquisition Enterprises B.V.",
    "averageHegemony": 0.7440694218654746,
    "dependentASNs": 17
  },
  {
    "providerASN": 34872,
    "providerName": "Servperso_Systems Sarah Rossius trading as Servperso Systems",
    "averageHegemony": 0.7280172413793103,
    "dependentASNs": 17
  },
  {
    "providerASN": 6453,
    "providerName": "AS6453 - TATA COMMUNICATIONS AMERICA INC",
    "averageHegemony": 0.510497833301183,
    "dependentASNs": 17
  },
  {
    "providerASN": 29467,
    "providerName": "LuxNetwork LUXNETWORK S.A.",
    "averageHegemony": 0.42224482308503275,
    "dependentASNs": 16
  },
  {
    "providerASN": 399486,
    "providerName": "VIRTUO - 12651980 CANADA INC.",
    "averageHegemony": 0.8509685230024212,
    "dependentASNs": 15
  },
  {
    "providerASN": 13335,
    "providerName": "CLOUDFLARENET - Cloudflare, Inc.",
    "averageHegemony": 0.6943162393162391,
    "dependentASNs": 14
  },
  {
    "providerASN": 209735,
    "providerName": "LAGRANGE Lagrange Cloud Technologies Limited",
    "averageHegemony": 0.8126942567567568,
    "dependentASNs": 13
  },
  {
    "providerASN": 3303,
    "providerName": "SWISSCOM Swisscom (Schweiz) AG",
    "averageHegemony": 0.3679940361057383,
    "dependentASNs": 13
  },
  {
    "providerASN": 32787,
    "providerName": "PROLEXIC-TECHNOLOGIES-DDOS-MITIGATION-NETWORK - Akamai Technologies, Inc.",
    "averageHegemony": 0.902790113719113,
    "dependentASNs": 12
  },
  {
    "providerASN": 34927,
    "providerName": "iFog-GmbH iFog GmbH",
    "averageHegemony": 0.7000000000000001,
    "dependentASNs": 12
  },
  {
    "providerASN": 24961,
    "providerName": "MYLOC-AS WIIT AG",
    "averageHegemony": 0.6184782608695651,
    "dependentASNs": 12
  },
  {
    "providerASN": 60144,
    "providerName": "THREE-W-INFRA-AS 3W Infra B.V.",
    "averageHegemony": 0.22727272727272724,
    "dependentASNs": 12
  },
  {
    "providerASN": 198949,
    "providerName": "Radware Radware Ltd",
    "averageHegemony": 0.6103896103896106,
    "dependentASNs": 11
  },
  {
    "providerASN": 8801,
    "providerName": "ROCKETFIBRE Rocket Fibre Ltd",
    "averageHegemony": 0.4189203202235118,
    "dependentASNs": 11
  },
  {
    "providerASN": 207841,
    "providerName": "INFERNO Inferno Communications Ltd",
    "averageHegemony": 0.21657226562499998,
    "dependentASNs": 11
  },
  {
    "providerASN": 702,
    "providerName": "UUNET - Verizon Business",
    "averageHegemony": 0.7934920634920636,
    "dependentASNs": 10
  },
  {
    "providerASN": 212895,
    "providerName": "ROUTE64_ORG Johannes Ernst",
    "averageHegemony": 0.790948275862069,
    "dependentASNs": 10
  },
  {
    "providerASN": 21351,
    "providerName": "CANALPLUSTELECOM Canal + Telecom SAS",
    "averageHegemony": 0.8361111111111111,
    "dependentASNs": 9
  },
  {
    "providerASN": 60068,
    "providerName": "CDN77 Datacamp Limited",
    "averageHegemony": 0.6304687500000001,
    "dependentASNs": 8
  },
  {
    "providerASN": 203446,
    "providerName": "AS203446 SMARTNET LIMITED",
    "averageHegemony": 0.4187229437229438,
    "dependentASNs": 5
  },
  {
    "providerASN": 210233,
    "providerName": "Pixinko Pixinko SARL",
    "averageHegemony": 0.38522727272727275,
    "dependentASNs": 5
  },
  {
    "providerASN": 33891,
    "providerName": "CORE-BACKBONE Core-Backbone GmbH",
    "averageHegemony": 0.2808333333333333,
    "dependentASNs": 5
  },
  {
    "providerASN": 4637,
    "providerName": "ASN-TELSTRA-GLOBAL Telstra Global",
    "averageHegemony": 0.19829545454545455,
    "dependentASNs": 5
  },
  {
    "providerASN": 2603,
    "providerName": "NORDUNET NORDUnet",
    "averageHegemony": 0.16388033510075428,
    "dependentASNs": 5
  },
  {
    "providerASN": 16509,
    "providerName": "AMAZON-02 - Amazon.com, Inc.",
    "averageHegemony": 1.0,
    "dependentASNs": 4
  },
  {
    "providerASN": 2686,
    "providerName": "ATGS-MMD-AS - AT&T Enterprises, LLC",
    "averageHegemony": 0.8291666666666668,
    "dependentASNs": 4
  },
  {
    "providerASN": 209533,
    "providerName": "BGPTunnel iFog GmbH",
    "averageHegemony": 0.6199999999999999,
    "dependentASNs": 4
  },
  {
    "providerASN": 5400,
    "providerName": "BT British Telecommunications PLC",
    "averageHegemony": 0.5021645021645021,
    "dependentASNs": 4
  },
  {
    "providerASN": 41051,
    "providerName": "FREETRANSIT Openfactory GmbH",
    "averageHegemony": 0.4375,
    "dependentASNs": 4
  },
  {
    "providerASN": 5405,
    "providerName": "INTERDOTLINK Inter.link GmbH",
    "averageHegemony": 0.435,
    "dependentASNs": 4
  },
  {
    "providerASN": 394177,
    "providerName": "SHIFT-HOSTING-LLC - SHIFT HOSTING LLC",
    "averageHegemony": 0.27307692307692305,
    "dependentASNs": 4
  },
  {
    "providerASN": 50263,
    "providerName": "IXP-1-IX-EU A-Systems Sp. z o.o.",
    "averageHegemony": 0.2727272727272727,
    "dependentASNs": 4
  },
  {
    "providerASN": 59796,
    "providerName": "STORMWALL-AS StormWall s.r.o.",
    "averageHegemony": 0.7722222222222221,
    "dependentASNs": 3
  }
]
```
---

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

> **Output (20 record(s)):**

```json
[
  {
    "localDomain": "ameli.fr",
    "percentageOfQueriesInCountry": 91.973244
  },
  {
    "localDomain": "louvre.fr",
    "percentageOfQueriesInCountry": 87.40458
  },
  {
    "localDomain": "huffingtonpost.fr",
    "percentageOfQueriesInCountry": 86.813187
  },
  {
    "localDomain": "doctolib.fr",
    "percentageOfQueriesInCountry": 82.938389
  },
  {
    "localDomain": "leroymerlin.fr",
    "percentageOfQueriesInCountry": 81.426814
  },
  {
    "localDomain": "lepoint.fr",
    "percentageOfQueriesInCountry": 76.404494
  },
  {
    "localDomain": "leboncoin.fr",
    "percentageOfQueriesInCountry": 75.0
  },
  {
    "localDomain": "impots.gouv.fr",
    "percentageOfQueriesInCountry": 75.0
  },
  {
    "localDomain": "vinted.fr",
    "percentageOfQueriesInCountry": 72.349061
  },
  {
    "localDomain": "labanquepostale.fr",
    "percentageOfQueriesInCountry": 70.707071
  },
  {
    "localDomain": "cic.fr",
    "percentageOfQueriesInCountry": 70.37037
  },
  {
    "localDomain": "cnil.fr",
    "percentageOfQueriesInCountry": 70.0
  },
  {
    "localDomain": "caf.fr",
    "percentageOfQueriesInCountry": 69.014085
  },
  {
    "localDomain": "sg.fr",
    "percentageOfQueriesInCountry": 66.666667
  },
  {
    "localDomain": "lemonde.fr",
    "percentageOfQueriesInCountry": 66.065574
  },
  {
    "localDomain": "tf1info.fr",
    "percentageOfQueriesInCountry": 65.306122
  },
  {
    "localDomain": "laredoute.fr",
    "percentageOfQueriesInCountry": 64.46281
  },
  {
    "localDomain": "rugbyrama.fr",
    "percentageOfQueriesInCountry": 64.285714
  },
  {
    "localDomain": "creditmutuel.fr",
    "percentageOfQueriesInCountry": 63.888889
  },
  {
    "localDomain": "lesechos.fr",
    "percentageOfQueriesInCountry": 62.666667
  }
]
```

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

> **Output (50 record(s)):**

```json
[
  {
    "hostingCountryCode": "US",
    "domainCount": 51
  },
  {
    "hostingCountryCode": "FR",
    "domainCount": 49
  },
  {
    "hostingCountryCode": "AU",
    "domainCount": 21
  },
  {
    "hostingCountryCode": "AF",
    "domainCount": 19
  },
  {
    "hostingCountryCode": "NL",
    "domainCount": 13
  },
  {
    "hostingCountryCode": "GB",
    "domainCount": 6
  },
  {
    "hostingCountryCode": "CH",
    "domainCount": 4
  },
  {
    "hostingCountryCode": "AT",
    "domainCount": 4
  },
  {
    "hostingCountryCode": "BG",
    "domainCount": 3
  },
  {
    "hostingCountryCode": "BR",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "IT",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "TR",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "MX",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "CO",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "CL",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "LT",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "UY",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "HK",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "KH",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "AE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "PA",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "AR",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "UA",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "RU",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "MU",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "KE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "RO",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "BH",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "AO",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "RS",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "SE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "DE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "DK",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "PH",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "LV",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "ES",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "SG",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "VN",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "LK",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "AD",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "CD",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "BE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "ZA",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "AZ",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "LU",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "TH",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "EE",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "EU",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "CA",
    "domainCount": 2
  },
  {
    "hostingCountryCode": "CZ",
    "domainCount": 1
  }
]
```
---

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

> **Output (25 record(s)):**

```json
[
  {
    "domainName": "ameli.fr",
    "percentageOfLocalQueries": 91.973244,
    "trancoRank": 4954
  },
  {
    "domainName": "louvre.fr",
    "percentageOfLocalQueries": 87.40458,
    "trancoRank": 6231
  },
  {
    "domainName": "huffingtonpost.fr",
    "percentageOfLocalQueries": 86.813187,
    "trancoRank": 5614
  },
  {
    "domainName": "doctolib.fr",
    "percentageOfLocalQueries": 82.938389,
    "trancoRank": 5094
  },
  {
    "domainName": "leroymerlin.fr",
    "percentageOfLocalQueries": 81.426814,
    "trancoRank": 1287
  },
  {
    "domainName": "lepoint.fr",
    "percentageOfLocalQueries": 76.404494,
    "trancoRank": 5703
  },
  {
    "domainName": "leboncoin.fr",
    "percentageOfLocalQueries": 75.0,
    "trancoRank": 1111
  },
  {
    "domainName": "impots.gouv.fr",
    "percentageOfLocalQueries": 75.0,
    "trancoRank": 8698
  },
  {
    "domainName": "vinted.fr",
    "percentageOfLocalQueries": 72.349061,
    "trancoRank": 1857
  },
  {
    "domainName": "labanquepostale.fr",
    "percentageOfLocalQueries": 70.707071,
    "trancoRank": 7772
  },
  {
    "domainName": "cic.fr",
    "percentageOfLocalQueries": 70.37037,
    "trancoRank": 8550
  },
  {
    "domainName": "cnil.fr",
    "percentageOfLocalQueries": 70.0,
    "trancoRank": 3428
  },
  {
    "domainName": "caf.fr",
    "percentageOfLocalQueries": 69.014085,
    "trancoRank": 6257
  },
  {
    "domainName": "sg.fr",
    "percentageOfLocalQueries": 66.666667,
    "trancoRank": 7474
  },
  {
    "domainName": "lemonde.fr",
    "percentageOfLocalQueries": 66.065574,
    "trancoRank": 693
  },
  {
    "domainName": "tf1info.fr",
    "percentageOfLocalQueries": 65.306122,
    "trancoRank": 6164
  },
  {
    "domainName": "laredoute.fr",
    "percentageOfLocalQueries": 64.46281,
    "trancoRank": 6867
  },
  {
    "domainName": "rugbyrama.fr",
    "percentageOfLocalQueries": 64.285714,
    "trancoRank": 9150
  },
  {
    "domainName": "creditmutuel.fr",
    "percentageOfLocalQueries": 63.888889,
    "trancoRank": 7616
  },
  {
    "domainName": "lesechos.fr",
    "percentageOfLocalQueries": 62.666667,
    "trancoRank": 3711
  },
  {
    "domainName": "radiofrance.fr",
    "percentageOfLocalQueries": 62.447257,
    "trancoRank": 3561
  },
  {
    "domainName": "lefigaro.fr",
    "percentageOfLocalQueries": 59.073359,
    "trancoRank": 813
  },
  {
    "domainName": "tf1.fr",
    "percentageOfLocalQueries": 57.687723,
    "trancoRank": 5851
  },
  {
    "domainName": "paris.fr",
    "percentageOfLocalQueries": 57.297297,
    "trancoRank": 6130
  },
  {
    "domainName": "meteociel.fr",
    "percentageOfLocalQueries": 57.142857,
    "trancoRank": 3765
  }
]
```

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

> **Output (0 record(s)):**

```json
[]
```

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

> **Output (2 record(s)):**

```json
[
  {
    "rpkiStatus": "RPKI Valid",
    "numberOfPrefixes": 1758
  },
  {
    "rpkiStatus": "RPKI NotFound",
    "numberOfPrefixes": 212
  }
]
```

---

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

> **Output (1 record(s)):**

```json
[
  {
    "totalASNs": 2238,
    "peeringASNs": 376,
    "peeringEfficiencyRatio": 0.1680071492403932
  }
]
```

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

> **Output (15 record(s)):**

```json
[
  {
    "ixpId": 3654261,
    "ixpName": "France-IX Paris",
    "localMemberCount": 235
  },
  {
    "ixpId": 3653469,
    "ixpName": "Equinix Paris",
    "localMemberCount": 151
  },
  {
    "ixpId": 3654213,
    "ixpName": "France-IX AURA",
    "localMemberCount": 59
  },
  {
    "ixpId": 3653957,
    "ixpName": "nine",
    "localMemberCount": 48
  },
  {
    "ixpId": 3653665,
    "ixpName": "France-IX Marseille",
    "localMemberCount": 37
  },
  {
    "ixpId": 3653633,
    "ixpName": "Lillix",
    "localMemberCount": 32
  },
  {
    "ixpId": 3654552,
    "ixpName": "Hopus",
    "localMemberCount": 27
  },
  {
    "ixpId": 3653687,
    "ixpName": "SFINX",
    "localMemberCount": 19
  },
  {
    "ixpId": 3654422,
    "ixpName": "BreizhIX",
    "localMemberCount": 18
  },
  {
    "ixpId": 3653428,
    "ixpName": "AuvernIX",
    "localMemberCount": 12
  },
  {
    "ixpId": 3654025,
    "ixpName": "DE-CIX Marseille",
    "localMemberCount": 10
  },
  {
    "ixpId": 3654000,
    "ixpName": "EuroRhine-IX",
    "localMemberCount": 10
  },
  {
    "ixpId": 3654383,
    "ixpName": "France-IX Lille",
    "localMemberCount": 10
  },
  {
    "ixpId": 3654425,
    "ixpName": "BGP.Exchange - Paris",
    "localMemberCount": 10
  },
  {
    "ixpId": 3653506,
    "ixpName": "Ouest.Network",
    "localMemberCount": 9
  }
]
```

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

> **Output (20 record(s)):**

```json
[
  {
    "asn": 1299,
    "asName": "TWELVE99 Arelion Sweden AB",
    "caidaRank": 2
  },
  {
    "asn": 3215,
    "asName": "AS3215 Orange S.A.",
    "caidaRank": 247
  },
  {
    "asn": 43531,
    "asName": "IXREACH BSO Network Solutions SAS",
    "caidaRank": 375
  },
  {
    "asn": 31216,
    "asName": "BSOCOM BSO Network Solutions SAS",
    "caidaRank": 376
  },
  {
    "asn": 43350,
    "asName": "NFORCE NForce Entertainment B.V.",
    "caidaRank": 1530
  },
  {
    "asn": 12844,
    "asName": "BOUYGTEL-B2B Bouygues Telecom SA",
    "caidaRank": 1945
  },
  {
    "asn": 198831,
    "asName": "HOLYCLOUD GENIUSWEER SAS",
    "caidaRank": 2233
  },
  {
    "asn": 48185,
    "asName": "team_blue team.blue NV",
    "caidaRank": 2251
  },
  {
    "asn": 39886,
    "asName": "STELOGY-INFRASTRUCTURE Nomotech SAS",
    "caidaRank": 2272
  },
  {
    "asn": 62610,
    "asName": "ZEN-DPS - Zenlayer Inc",
    "caidaRank": 2393
  },
  {
    "asn": 206120,
    "asName": "KOESIO-NETWORKS KOESIO Networks SAS",
    "caidaRank": 2637
  },
  {
    "asn": 31221,
    "asName": "NLT-FR nLighten France SAS",
    "caidaRank": 3139
  },
  {
    "asn": 29066,
    "asName": "VELIANET-AS velia.net Internetdienste GmbH",
    "caidaRank": 3265
  },
  {
    "asn": 200780,
    "asName": "APPLIWAVE Eurofiber France SAS",
    "caidaRank": 3396
  },
  {
    "asn": 12670,
    "asName": "AS-COMPLETEL Completel SAS",
    "caidaRank": 3459
  },
  {
    "asn": 52073,
    "asName": "I2SNETWORK I2SNETWORK SAS",
    "caidaRank": 3586
  },
  {
    "asn": 33392,
    "asName": "DAUPHIN-TELECOM - Dauphin Telecom",
    "caidaRank": 4448
  },
  {
    "asn": 215114,
    "asName": "PLB-NET Stevan Durand--L'Hours t/a SLBCLOUD",
    "caidaRank": 4680
  },
  {
    "asn": 5583,
    "asName": "ORANGE-BUSINESS-SERVICES-BENELUX Orange S.A.",
    "caidaRank": 4729
  },
  {
    "asn": 57179,
    "asName": "IELO-B",
    "caidaRank": 5079
  }
]
```

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

> **Output (8 record(s)):**

```json
[
  {
    "numberOfIXPsMemberOf": 12,
    "numberOfASes": 1
  },
  {
    "numberOfIXPsMemberOf": 9,
    "numberOfASes": 1
  },
  {
    "numberOfIXPsMemberOf": 6,
    "numberOfASes": 10
  },
  {
    "numberOfIXPsMemberOf": 5,
    "numberOfASes": 7
  },
  {
    "numberOfIXPsMemberOf": 4,
    "numberOfASes": 19
  },
  {
    "numberOfIXPsMemberOf": 3,
    "numberOfASes": 47
  },
  {
    "numberOfIXPsMemberOf": 2,
    "numberOfASes": 97
  },
  {
    "numberOfIXPsMemberOf": 1,
    "numberOfASes": 194
  }
]
```

---

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
  },
  {
    "type(r)": "TARGET"
  },
  {
    "type(r)": "WEBSITE"
  }
]
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