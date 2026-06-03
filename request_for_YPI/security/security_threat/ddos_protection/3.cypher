MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)

WITH d, q.value AS queryPercentage
ORDER BY queryPercentage DESC
LIMIT 20

MATCH (d)<-[:PART_OF]-(h:HostName)
MATCH (h)-[:RESOLVES_TO]->(ip:IP)
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)
MATCH (hostAS:AS)-[:ORIGINATE]->(pfx)

MATCH (hostAS)-[:CATEGORIZED]->(cat:Tag)
WHERE cat.label IN ["Content Delivery Network","DDoS Mitigation"]

OPTIONAL MATCH (hostAS)-[:NAME]->(n:Name)

WITH
    d.name AS popularDomain,
    hostAS.asn AS hostingASN,
    collect(DISTINCT cat.label) AS protections,
    collect(DISTINCT n.name)[0] AS hostingName,
    max(queryPercentage) AS queryPercentage

RETURN DISTINCT
       popularDomain,
       hostingASN,
       hostingName,
       protections,
       queryPercentage
ORDER BY queryPercentage DESC
LIMIT 20;