// Multi-location operators — counts ASes with presence in more than one geographic Point.
// An AS declared in multiple geographic locations operates physical infrastructure
// in multiple places, a strong signal of real geographic network reach (fiber deployment).
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:LOCATED_IN]->(p:Point)
WHERE (a)-[:ORIGINATE]->(:BGPPrefix)
WITH a, count(DISTINCT p) AS locationCount
WHERE locationCount > 1
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
RETURN a.asn AS ASN,
       n.name AS operatorName,
       locationCount AS numberOfLocations
ORDER BY locationCount DESC;
