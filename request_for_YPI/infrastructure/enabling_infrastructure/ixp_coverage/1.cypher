// Lists all Internet Exchange Points (IXPs) located in a country,
// along with the data center facilities where each IXP is hosted.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (i:IXP)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (i)-[:LOCATED_IN]->(f:Facility)
RETURN i.name AS IXP, COLLECT(DISTINCT f.name) AS Facilities
ORDER BY SIZE(Facilities) DESC;