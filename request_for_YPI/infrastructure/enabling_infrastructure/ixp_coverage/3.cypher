// Finds the top foreign networks (by CAIDA ASRank) that are members of IXPs
// located in the country. Shows their global importance rank and which local
// IXPs they participate in. Indicates whether the country is a regional peering hub.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(ic:Country {country_code: $countryCode})
MATCH (i)<-[:MEMBER_OF]-(a:AS)
OPTIONAL MATCH (a)-[:COUNTRY]->(ac:Country)
WITH i, a, COLLECT(DISTINCT ac.country_code) AS member_countries
WHERE NOT $countryCode IN member_countries
OPTIONAL MATCH (a)-[rel:RANK]->(r:Ranking {name: 'CAIDA ASRank'})
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a.asn AS ASN, MIN(n.name) AS NetworkName, COLLECT(DISTINCT i.name) AS IXPs, MIN(rel.rank) AS CaidaRank
WHERE CaidaRank IS NOT NULL
RETURN ASN, NetworkName, IXPs, CaidaRank
ORDER BY CaidaRank ASC
LIMIT 15;