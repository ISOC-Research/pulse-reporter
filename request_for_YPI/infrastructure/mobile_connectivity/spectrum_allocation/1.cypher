// Spectrum allocation: prefixes originated by ASes in the country.

MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:ORIGINATE]->(p:BGPPrefix)
RETURN c.name AS Country,
       COUNT(DISTINCT p) AS Originated_Prefixes;
