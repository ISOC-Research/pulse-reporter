// HTTPS adoption among locally queried domains

MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
WITH count(DISTINCT d) AS totalQueried

MATCH (c:Country {country_code: $countryCode})<-[q2:QUERIED_FROM]-(d:DomainName)
MATCH (h:HostName)-[:PART_OF]->(d)
MATCH (u:URL)-[:PART_OF]->(h)

WHERE u.url STARTS WITH 'https'

WITH totalQueried,
     count(DISTINCT d) AS httpsDomains

RETURN
    totalQueried,
    httpsDomains AS httpsCount,
    httpsDomains AS resolvedDomains,
    CASE
        WHEN totalQueried = 0 THEN 0.0
        ELSE round((toFloat(httpsDomains) / totalQueried) * 100.0, 2)
    END AS httpsAdoptionRate