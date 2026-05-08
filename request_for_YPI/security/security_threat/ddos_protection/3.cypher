// Identifies popular domains in a country and checks if they are hosted by a CDN or DDoS-mitigating AS.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'DE', 'BR').
// Finds the most queried domains from the country.
MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
WITH d, q.value AS queryPercentage ORDER BY queryPercentage DESC LIMIT 20
// Finds the AS announcing the IP of these domains.
MATCH (d)-[:RESOLVES_TO]->(ip:IP)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostAS:AS)
// Checks if this AS is a CDN or DDoS mitigation provider.
WHERE (hostAS)-[:CATEGORIZED]->(:Tag {label: "Content Delivery Network"})
   OR (hostAS)-[:CATEGORIZED]->(:Tag {label: "DDoS Mitigation"})
OPTIONAL MATCH (hostAS)-[:NAME]->(n:Name)
OPTIONAL MATCH (hostAS)-[:CATEGORIZED]->(cat:Tag) WHERE cat.label IN ["Content Delivery Network", "DDoS Mitigation"]
RETURN d.name AS popularDomain,
       hostAS.asn AS hostingCdnASN,
       n.name AS hostingCdnName,
       cat.label AS hostingType,
       queryPercentage
ORDER BY queryPercentage DESC;