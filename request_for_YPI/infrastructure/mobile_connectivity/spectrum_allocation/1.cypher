// BGP prefix count breakdown by address family — measures IP address space utilization.
// IPv4 prefix count shows existing deployment scale; IPv6 prefix count shows
// forward-looking address space adoption and future network capacity planning.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(p:BGPPrefix)
RETURN c.name AS Country,
       count(DISTINCT p)                                                    AS Originated_Prefixes,
       count(DISTINCT CASE WHEN p.af = 4 THEN p ELSE null END)             AS IPv4_Prefixes,
       count(DISTINCT CASE WHEN p.af = 6 THEN p ELSE null END)             AS IPv6_Prefixes,
       count(DISTINCT as)                                                   AS ActiveOperators,
       round(100.0 * count(DISTINCT CASE WHEN p.af = 6 THEN p ELSE null END)
             / count(DISTINCT p), 2)                                        AS IPv6_SharePercent
ORDER BY Originated_Prefixes DESC;
