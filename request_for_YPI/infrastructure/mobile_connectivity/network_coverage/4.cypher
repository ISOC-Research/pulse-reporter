// Peering density analysis: breaks down peering connections into domestic
// (both ASes in the same country) vs international. High domestic peering
// means local traffic stays local; low domestic peering means traffic
// must route internationally — a critical resilience weakness.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:PEERS_WITH]-(b:AS)
OPTIONAL MATCH (b)-[:COUNTRY]->(bc:Country)
WITH c, b, COLLECT(DISTINCT bc.country_code) AS PeerCountries
RETURN c.name AS Country,
       COUNT(DISTINCT CASE WHEN $countryCode IN PeerCountries THEN b END) AS DomesticPeers,
       COUNT(DISTINCT CASE WHEN NOT $countryCode IN PeerCountries THEN b END) AS InternationalPeers,
       COUNT(DISTINCT b) AS TotalPeers;
