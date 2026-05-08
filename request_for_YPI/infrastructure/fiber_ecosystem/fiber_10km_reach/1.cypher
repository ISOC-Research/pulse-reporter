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
