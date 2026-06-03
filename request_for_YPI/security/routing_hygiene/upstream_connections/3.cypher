// Concentration of upstream providers

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as_fr:AS)

MATCH (as_fr)-[:PEERS_WITH]-(peer:AS)

MATCH (peer)-[:COUNTRY]->(peer_country:Country)

WHERE peer_country <> c

WITH
    peer,
    collect(DISTINCT peer_country.country_code)[0] AS upstreamCountry,
    count(DISTINCT as_fr) AS connectedDomesticClients

RETURN
    peer.asn AS upstreamAS,
    upstreamCountry,
    connectedDomesticClients

ORDER BY connectedDomesticClients DESC
LIMIT 10