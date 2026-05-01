// Lists all IXPs in a country and the cities where they are present.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'BR', 'DE').
MATCH (i:IXP)<-[:MEMBER_OF]-(a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (a)-[:LOCATED_IN]->(f:Facility)
RETURN i.name AS IXP, COLLECT(DISTINCT f.name) AS Cities
ORDER BY IXP;