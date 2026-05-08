// IPv6 population coverage rate — measures what percentage of the country's population
// is served by ASes that announce at least one IPv6 prefix. This is the population-weighted
// metric aligned with ITU's IPv6 adoption measurement methodology.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'BE', 'CA').
MATCH (c:Country {country_code: $countryCode})<-[pop:POPULATION]-(as:AS)
WITH c, sum(pop.percent) AS totalCoveredPopulationPct

MATCH (c:Country {country_code: $countryCode})<-[pop2:POPULATION]-(as2:AS)
WHERE (as2)-[:ORIGINATE]->(:BGPPrefix {af: 6})
WITH c, totalCoveredPopulationPct, sum(pop2.percent) AS ipv6CoveredPopulationPct

RETURN c.name AS country,
       round(totalCoveredPopulationPct, 2)  AS totalCoveredPopulationPct,
       round(ipv6CoveredPopulationPct, 2)   AS ipv6CoveredPopulationPct,
       CASE
           WHEN totalCoveredPopulationPct = 0 THEN 0
           ELSE round((ipv6CoveredPopulationPct / totalCoveredPopulationPct) * 100.0, 2)
       END AS ipv6PopulationCoverageRate;
