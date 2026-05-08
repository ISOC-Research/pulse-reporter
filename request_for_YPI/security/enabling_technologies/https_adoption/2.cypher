// HTTPS adoption rate for locally queried domains.
// Measures what percentage of the most-queried domains in a country resolve via HTTPS
// by checking if the domain name starts with 'https' in the origin field of the ranking.
// Complements query 1 (Google CrUX-based) with locally-measured DNS query data.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
WITH count(DISTINCT d) AS totalQueried

MATCH (c:Country {country_code: $countryCode})<-[q2:QUERIED_FROM]-(d2:DomainName)
WHERE d2.name STARTS WITH 'https' OR (d2)-[:RESOLVES_TO]->(:IP)
WITH totalQueried,
     count(DISTINCT CASE WHEN d2.name STARTS WITH 'https' THEN d2 ELSE null END) AS httpsCount,
     count(DISTINCT d2) AS resolvedDomains

RETURN totalQueried,
       httpsCount,
       resolvedDomains,
       CASE
           WHEN totalQueried = 0 THEN 0
           ELSE round((toFloat(httpsCount) / totalQueried) * 100.0, 2)
       END AS httpsAdoptionRate;
