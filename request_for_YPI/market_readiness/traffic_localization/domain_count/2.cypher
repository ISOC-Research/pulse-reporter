// Analyses the geographic distribution of hosting for the top 100 ccTLD domains.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Focus on popular domains (source: Tranco) for a relevant analysis.
MATCH (d)-[r:RANK]->(:Ranking {name:"Tranco top 1M"})
WITH d ORDER BY r.rank LIMIT 100

// Expand search to include the domain itself, its subdomains, and its hostnames
OPTIONAL MATCH (d)-[:RESOLVES_TO]->(ip1:IP)
OPTIONAL MATCH (d)<-[:PARENT*1..2]-(sub:DomainName)-[:RESOLVES_TO]->(ip2:IP)
OPTIONAL MATCH (d)-[:MANAGED_BY]->(h:HostName)-[:RESOLVES_TO]->(ip3:IP)

WITH d, coalesce(ip1, ip2, ip3) AS ip
WHERE ip IS NOT NULL

// Trace hosting country via the confirmed IYP path
MATCH (ip)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)
MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

WITH hostingCountry, count(DISTINCT d) AS domainCount
RETURN hostingCountry.country_code AS hostingCountryCode,
       domainCount
ORDER BY domainCount DESC;