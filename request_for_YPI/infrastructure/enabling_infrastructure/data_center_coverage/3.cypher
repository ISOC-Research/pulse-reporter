// Finds the top 10 most important ASes in a country that are not members of any local IXP.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'BR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
WHERE NOT (a)-[:MEMBER_OF]->(:IXP)
RETURN a.asn AS ASN
ORDER BY a.asn ASC
LIMIT 10;