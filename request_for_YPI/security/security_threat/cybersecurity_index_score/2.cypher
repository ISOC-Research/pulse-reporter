// Measures the PeeringDB presence rate of ASes in a country.
// A PeeringDB entry indicates a network is organized, documented, and open to coordination.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)
WITH c, collect(DISTINCT as) AS allASes

// Unwind and check for the presence of a PeeringDB ID
UNWIND allASes AS as
OPTIONAL MATCH (as)-[:EXTERNAL_ID]->(pdb:PeeringdbNetID)

WITH c,
     count(as) AS totalAS,
     count(pdb) AS asWithPeeringDB

// Calculate the percentage
RETURN c.name AS country,
       totalAS,
       asWithPeeringDB,
       CASE
           WHEN totalAS = 0 THEN 0
           ELSE (toFloat(asWithPeeringDB) / totalAS) * 100.0
       END AS coordinationPercentage
ORDER BY coordinationPercentage DESC