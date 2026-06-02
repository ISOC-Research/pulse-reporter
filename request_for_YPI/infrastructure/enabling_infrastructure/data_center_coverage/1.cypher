// Lists all data center facilities (colocation facilities) in a country,
// along with the count of ASes colocated at each facility.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (f:Facility)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (a:AS)-[:LOCATED_IN]->(f)
RETURN f.name AS DataCenter, COUNT(DISTINCT a) AS ColocatedASes
ORDER BY ColocatedASes DESC;