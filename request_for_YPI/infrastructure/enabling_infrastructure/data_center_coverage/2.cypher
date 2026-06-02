// For each data center in the country, lists the operator (organization) that manages it.
// Helps assess whether the data center market is dominated by one or a few operators (concentration risk).
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (f:Facility)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (f)-[:MANAGED_BY]->(org:Organization)
RETURN org.name AS Operator, COUNT(DISTINCT f) AS DataCenterCount
ORDER BY DataCenterCount DESC;
