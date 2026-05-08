// Analyses the geographic distribution of hosting for the top 100 ccTLD domains.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Focus on popular domains (source: Tranco) for a relevant analysis.
MATCH (d)-[r:RANK]->(:Ranking {name:"Tranco top 1M"})
WITH d ORDER BY r.rank LIMIT 100

// Trace hosting country via: DomainName -> IP -[:PART_OF]-> BGPPrefix <- [:ORIGINATE]- AS -> Country
MATCH (d)-[:RESOLVES_TO]->(ip:IP)-[:PART_OF]->(pfx:BGPPrefix)<-[:ORIGINATE]-(hostingAS:AS)
MATCH (hostingAS)-[:COUNTRY]->(hostingCountry:Country)

WITH hostingCountry, count(DISTINCT d) AS domainCount
RETURN hostingCountry.country_code AS hostingCountryCode,
       domainCount
ORDER BY domainCount DESC;