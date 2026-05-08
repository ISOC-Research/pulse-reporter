// Calculates the Herfindahl-Hirschman Index (HHI) for a country's internet market.
// HHI = sum of squared market shares. Higher HHI = more concentrated market.
// Thresholds: <1500 = Competitive, 1500-2500 = Moderately Concentrated, >2500 = Highly Concentrated.
// The parameter $countryCode must be provided during execution (e.g., 'CI', 'FR', 'KE').
MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)
WITH c, sum(p.percent^2) AS hhi, count(DISTINCT as) AS totalAS
RETURN hhi,
       totalAS,
       CASE
           WHEN hhi < 1500 THEN 'Competitive Market'
           WHEN hhi >= 1500 AND hhi <= 2500 THEN 'Moderately Concentrated Market'
           ELSE 'Highly Concentrated Market'
       END AS marketConcentration;