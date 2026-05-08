// Retrieves popular domains hosted on infrastructure in the target country via BGP prefix ownership.
// Uses the valid IYP path: AS (in country) -[:ORIGINATE]-> BGPPrefix <- [:PART_OF]- IP <- [:RESOLVES_TO]- DomainName
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(pfx:BGPPrefix)<-[:PART_OF]-(ip:IP)<-[:RESOLVES_TO]-(d:DomainName)
// Filter by Tranco ranking for popular domains only.
MATCH (d)-[r:RANK]->(rk:Ranking)
WHERE rk.name CONTAINS 'Tranco'
RETURN d.name AS domainName,
       r.rank AS popularityRank,
       as.asn AS hostingASN
ORDER BY r.rank ASC
LIMIT 25;