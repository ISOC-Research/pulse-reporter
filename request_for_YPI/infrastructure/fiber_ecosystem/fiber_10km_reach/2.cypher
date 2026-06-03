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
