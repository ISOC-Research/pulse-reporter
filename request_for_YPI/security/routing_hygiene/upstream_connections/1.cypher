// Identifies transit providers of a country and ranks them by CAIDA ASRank.

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(local_as:AS)

MATCH (local_as)-[:PEERS_WITH {rel: 1}]->(provider:AS)

WHERE NOT (provider)-[:COUNTRY]->(c)

WITH provider, count(DISTINCT local_as) AS local_clients

OPTIONAL MATCH (provider)-[r:RANK]->(:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (provider)-[:NAME]->(n:Name)

WITH
    provider,
    local_clients,
    r.rank AS caidaASRank,
    collect(DISTINCT n.name)[0] AS providerName

RETURN
    provider.asn AS providerASN,
    providerName,
    local_clients,
    caidaASRank

ORDER BY caidaASRank ASC, local_clients DESC
LIMIT 20;