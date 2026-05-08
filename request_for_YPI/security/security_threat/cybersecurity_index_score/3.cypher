// Internet hegemony concentration — measures how dependent a country's ASes are
// on a small number of upstream providers. A high hegemony score for a single provider
// means the country's internet traffic is heavily routed through that one AS,
// creating a critical single point of failure and cybersecurity risk.
// Uses IHR (Internet Health Report) hegemony data from the DEPENDS_ON relationship.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(localAS:AS)
MATCH (localAS)-[d:DEPENDS_ON]->(provider:AS)
WHERE d.hege > 0.05
  AND NOT (provider)-[:COUNTRY]->(c)

WITH provider,
     count(DISTINCT localAS) AS dependentLocalASes,
     avg(d.hege)             AS avgHegemonyScore,
     max(d.hege)             AS maxHegemonyScore

OPTIONAL MATCH (provider)-[:NAME]->(n:Name)
OPTIONAL MATCH (provider)-[:COUNTRY]->(providerCountry:Country)

RETURN provider.asn           AS providerASN,
       n.name                 AS providerName,
       providerCountry.country_code AS providerCountry,
       dependentLocalASes,
       round(avgHegemonyScore, 4) AS avgHegemonyScore,
       round(maxHegemonyScore, 4) AS maxHegemonyScore
ORDER BY avgHegemonyScore DESC
LIMIT 10