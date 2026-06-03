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