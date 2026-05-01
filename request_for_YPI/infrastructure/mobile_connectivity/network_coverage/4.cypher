// Measures network coverage via peering between local ASes.

MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:PEERS_WITH]-(b:AS)
RETURN c.name AS Country,
       COUNT(DISTINCT b) AS TotalPeerings;
