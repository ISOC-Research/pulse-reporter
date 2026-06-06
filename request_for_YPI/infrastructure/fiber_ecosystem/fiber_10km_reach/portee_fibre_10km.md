### Analysis of the FRI (Fiber Reach Index) Indicator

This indicator from the "Infrastructure" pillar evaluates the geographic reach of the fiber optic network within a country. The objective is to assess the density and proximity of connectivity infrastructures that enable high-speed services (fiber, IP backbones) to effectively reach populated areas. A denser distribution of physical network nodes and local interconnections indicates a broader fiber footprint, meaning that fiber backbones are available closer to operators and potentially end-users.

The key technical entities involved are:
* `:AS` (Autonomous Systems, representing network operators)
* `:Point` (geographic points or physical network nodes)
* `:Facility` (physical data center/colocation nodes)
* `:BGPPrefix` (announced IP blocks indicating routing activity)

### YPI Relevance and Technical Analysis Plan

* **Relevance Assessment:** Case B (Relevant but partial). The YPI (Your Peering Intelligence) schema does not contain direct physical telemetry on fiber cables (such as physical route length, topology, or channel capacities). However, it offers a robust structural proxy via geographic points (:Point), data center facility footprints (:Facility), and BGP prefix allocations. These elements allow a realistic approximation of fiber reach by analyzing the physical and logical distribution of active network operators.

Here is the technical analysis plan for this indicator:

#### Query 1: Fiber Infrastructure Geographic Reach (Active Operator Points)

* **Query Objective:** This query approximates physical fiber reach by counting the number of distinct geographic Points associated with active Autonomous Systems (operators that actively announce BGP prefixes). A higher number of geographic points spread across active operators indicates a broader physical network footprint and suggests a wider fiber deployment reach.

* **Cypher Query:**
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

#### Query 2: Network Operators by Routing Footprint and Physical Presence

* **Query Objective:** This query ranks the country's active network operators by their routing footprint (BGP prefixes announced) combined with their physical facility presence (number of data center facilities they occupy). Operators possessing both high BGP prefix counts and presence across multiple facilities represent the backbone of the country's fiber infrastructure.

* **Cypher Query:**
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

#### Query 3: Multi-Facility Network Operators

* **Query Objective:** This query identifies network operators colocated in more than one physical facility within the country. An active operator present across multiple facilities demonstrates physically distributed infrastructure, which is a strong indicator of real geographic reach and fiber backbone diversity beyond a single central office.

* **Cypher Query:**
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

### Overall Analysis Objective

Executing these queries provides a functional picture of the country's fiber and backbone network reach:
1. **Query 1** measures physical footprint (geographic presence of active networks).
2. **Query 2** measures logical vs. physical scale (major operators and their facilities).
3. **Query 3** highlights infrastructure distribution (operators with redundant, multi-site presence).

Combining these dimensions helps analysts determine if the fiber ecosystem is well-distributed, resilient, or concentrated in a single geographic hub.

### Strategic Interpretation

| Observed Situation | Possible Interpretation |
|---|---|
| High GeoCoveragePoints + strong multi-facility operator base | Broad fiber reach, competitive market, and high geographic resilience. |
| Low GeoCoveragePoints + high operator concentration | Fiber infrastructure is concentrated in a few urban centers, leaving other regions underserved. |
| High GeoCoveragePoints + low facility diversity | Wide geographic coverage, but high risk of single-point-of-failure outages due to facility concentration. |
| Low GeoCoveragePoints + low facility presence | Underdeveloped backbone ecosystem, high reliance on foreign infrastructure or single-transit providers. |

### Policy Recommendations

* **If geographic points (Query 1) are low:** Encourage public-private partnerships or grant infrastructure concessions to expand fiber backhauls to secondary cities and rural areas.
* **If facility presence (Query 2/3) is low:** Promote the construction of local carrier-neutral facilities to incentivize operators to distribute their points of presence (PoPs), improving regional routing redundancy.