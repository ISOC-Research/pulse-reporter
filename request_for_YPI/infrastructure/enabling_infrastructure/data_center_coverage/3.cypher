// Identifies the most significant ASes in the country that are not colocated in any
// data center facility. Ranked by prefix count (routing footprint) so the most
// infrastructure-relevant networks appear first.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
WHERE NOT (a)-[:LOCATED_IN]->(:Facility)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)
WITH a, MIN(n.name) AS NetworkName, COUNT(DISTINCT pfx) AS PrefixCount
RETURN DISTINCT a.asn AS ASN, NetworkName, PrefixCount
ORDER BY PrefixCount DESC
LIMIT 20;