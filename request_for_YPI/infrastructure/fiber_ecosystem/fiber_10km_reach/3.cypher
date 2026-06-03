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
