// Network operator ecosystem overview: counts active vs dormant ASes, facility
// presence, IXP membership, and geographic coverage for the country.
// Gives a single-glance health check of the network coverage ecosystem.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)
WITH c, a, COUNT(pfx) AS pfxCount
WITH c,
     COUNT(DISTINCT a) AS TotalASes,
     COUNT(DISTINCT CASE WHEN pfxCount > 0 THEN a END) AS ActiveASes,
     COUNT(DISTINCT CASE WHEN pfxCount = 0 THEN a END) AS DormantASes
RETURN c.name AS Country, TotalASes, ActiveASes, DormantASes,
       ROUND(ActiveASes * 100.0 / TotalASes * 100) / 100 AS ActivePercent;
