// Query 2: Hosting Analysis — traces the AS and country hosting a given domain.
// The $domainName and $countryCode parameters must be provided during execution.
MATCH (d:DomainName {name: $domainName})
// Expand search to include the domain itself, its subdomains, and its hostnames
OPTIONAL MATCH (d)-[:RESOLVES_TO]->(ip1:IP)
OPTIONAL MATCH (d)<-[:PARENT*1..2]-(sub:DomainName)-[:RESOLVES_TO]->(ip2:IP)
OPTIONAL MATCH (d)-[:MANAGED_BY]->(h:HostName)-[:RESOLVES_TO]->(ip3:IP)

WITH coalesce(ip1, ip2, ip3) AS ip
WHERE ip IS NOT NULL

// Trace the hosting AS via the confirmed IYP path: IP -[:PART_OF]-> BGPPrefix <- [:ORIGINATE]- AS
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)

OPTIONAL MATCH (hostingAS)-[:NAME]->(n:Name)
OPTIONAL MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

WITH hostingAS, hostingCountry, collect(DISTINCT n.name)[0] AS hostingASName
RETURN DISTINCT
       hostingAS.asn AS hostingASN,
       hostingASName,
       hostingCountry.country_code AS hostingASCountry,
       (hostingCountry.country_code = $countryCode) AS isHostedLocally
LIMIT 10;