// Counts the local and international members for each IXP in a country.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (i:IXP)<-[:MEMBER_OF]-(a:AS)-[:COUNTRY]->(c:Country)
WITH i, c, a, (CASE WHEN c.country_code = $countryCode THEN 1 ELSE 0 END) AS local
WHERE c.country_code IS NOT NULL
RETURN i.name AS IXP,
       SUM(local) AS LocalMembers,
       COUNT(DISTINCT a) - SUM(local) AS ForeignMembers
ORDER BY LocalMembers DESC;