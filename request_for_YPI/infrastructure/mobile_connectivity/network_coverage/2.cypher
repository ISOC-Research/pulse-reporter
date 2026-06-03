// Physical infrastructure footprint: counts domestic vs international facilities
// where the country's ASes are colocated. Domestic facility count measures local
// infrastructure depth; international presence shows global connectivity reach.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
MATCH (a)-[:LOCATED_IN]->(f:Facility)
OPTIONAL MATCH (f)-[:COUNTRY]->(fc:Country)
WITH c, f, fc.country_code AS FacilityCountry
RETURN c.name AS Country,
       COUNT(DISTINCT CASE WHEN FacilityCountry = $countryCode THEN f END) AS DomesticFacilities,
       COUNT(DISTINCT CASE WHEN FacilityCountry <> $countryCode THEN f END) AS InternationalFacilities,
       COUNT(DISTINCT f) AS TotalFacilities;
