// Counts the number of local AS members for each IXP in a given country.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'BR', 'DE').
MATCH (a:AS)-[:MEMBER_OF]->(i:IXP), (a)-[:COUNTRY]->(c:Country {country_code: $countryCode})
RETURN i.name AS IXP, COUNT(DISTINCT a) AS LocalMembers
ORDER BY LocalMembers DESC;
