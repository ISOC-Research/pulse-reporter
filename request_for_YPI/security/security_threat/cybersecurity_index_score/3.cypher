// Internet hegemony concentration

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

WITH provider,
     collect(DISTINCT n.name)[0] AS providerName,
     collect(DISTINCT providerCountry.country_code)[0] AS providerCountry,
     dependentLocalASes,
     avgHegemonyScore,
     maxHegemonyScore

RETURN
       provider.asn AS providerASN,
       providerName,
       providerCountry,
       dependentLocalASes,
       round(avgHegemonyScore, 4) AS avgHegemonyScore,
       round(maxHegemonyScore, 4) AS maxHegemonyScore

ORDER BY dependentLocalASes DESC,
         avgHegemonyScore DESC
LIMIT 10