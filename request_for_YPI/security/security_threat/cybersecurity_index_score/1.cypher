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