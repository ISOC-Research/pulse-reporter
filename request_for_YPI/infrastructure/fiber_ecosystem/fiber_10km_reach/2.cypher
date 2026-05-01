// Approximates fiber proximity: number of local network neighbors.
// The more PEERS_WITH connections an AS has, the shorter its "reach".

MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:PEERS_WITH]-(b:AS)
RETURN a.asn AS ASN,
       COUNT(DISTINCT b) AS LocalNeighbors
ORDER BY LocalNeighbors DESC
LIMIT 20;

