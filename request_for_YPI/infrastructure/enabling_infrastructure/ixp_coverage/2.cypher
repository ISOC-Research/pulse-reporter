// Counts the local and international AS members for each IXP located in a country.
// Local = AS also registered in the same country. Foreign = AS from another country.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(ic:Country {country_code: $countryCode})
MATCH (i)<-[:MEMBER_OF]-(a:AS)
OPTIONAL MATCH (a)-[:COUNTRY]->(ac:Country)
WITH i, a, COLLECT(DISTINCT ac.country_code) AS member_countries
WITH i,
     COUNT(DISTINCT CASE WHEN $countryCode IN member_countries THEN a END) AS LocalMembers,
     COUNT(DISTINCT CASE WHEN NOT $countryCode IN member_countries THEN a END) AS ForeignMembers
RETURN i.name AS IXP, LocalMembers, ForeignMembers
ORDER BY LocalMembers DESC;