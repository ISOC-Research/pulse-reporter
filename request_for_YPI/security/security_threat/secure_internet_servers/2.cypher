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