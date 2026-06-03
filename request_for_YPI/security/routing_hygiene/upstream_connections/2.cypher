MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(local_as:AS)
MATCH (local_as)-[:PEERS_WITH {rel: 1}]->(provider:AS)
WHERE NOT (provider)-[:COUNTRY]->(c)

WITH DISTINCT provider

OPTIONAL MATCH (provider)-[r:RANK]->(:Ranking {name: 'CAIDA ASRank'})

WITH CASE
    WHEN r.rank IS NULL THEN 'E) Unranked'
    WHEN r.rank <= 100 THEN 'A) Top 100 (Internet Core)'
    WHEN r.rank <= 500 THEN 'B) Top 101-500 (Major)'
    WHEN r.rank <= 2000 THEN 'C) Top 501-2000 (Important)'
    ELSE 'D) Beyond 2000 (Regional/Niche)'
END AS providerTier

RETURN
    providerTier,
    count(*) AS numberOfProviders
ORDER BY providerTier;