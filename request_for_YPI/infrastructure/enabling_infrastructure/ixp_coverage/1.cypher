// Lists the IXPs of a country and the data centers where they are located.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (i:IXP)<-[:MEMBER_OF]-(a:AS)-[:LOCATED_IN]->(f:Facility),
      (a)-[:COUNTRY]->(c:Country {country_code: $countryCode})
RETURN i.name AS IXP, COLLECT(DISTINCT f.name) AS Facilities
ORDER BY SIZE(Facilities) DESC;