// Query 2: Hosting Analysis — traces the AS and country hosting a given domain.
// The $domainName and $countryCode parameters must be provided during execution.
MATCH (d:DomainName {name: $domainName})
MATCH (d)-[:RESOLVES_TO]->(ip:IP)

// Trace the hosting AS via the confirmed IYP path: IP -[:PART_OF]-> BGPPrefix <- [:ORIGINATE]- AS
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)

OPTIONAL MATCH (hostingAS)-[:NAME]->(n:Name)
OPTIONAL MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

RETURN DISTINCT
       hostingAS.asn AS hostingASN,
       n.name AS hostingASName,
       hostingCountry.country_code AS hostingASCountry,
       (hostingCountry.country_code = $countryCode) AS isHostedLocally
LIMIT 10;