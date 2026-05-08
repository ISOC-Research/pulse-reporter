// BGP prefix count per active AS — a proxy for geographic network coverage depth.
// Operators with more BGP prefixes have finer-grained network segmentation,
// typically indicating a broader physical footprint and more granular routing control.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a, n, count(DISTINCT p) AS prefixCount
WHERE prefixCount > 0
RETURN a.asn AS ASN,
       n.name AS operatorName,
       prefixCount AS announcedPrefixes
ORDER BY announcedPrefixes DESC
LIMIT 20;

