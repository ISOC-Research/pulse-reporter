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
