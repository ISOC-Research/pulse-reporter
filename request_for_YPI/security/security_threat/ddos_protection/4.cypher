// 4. Diversity of Internet Exchange Points (IXP) in a country.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'DE', 'BR').
MATCH (c:Country {country_code: $countryCode})

// Find IXPs located in the country.
MATCH (ixp:IXP)-[:COUNTRY]->(c)

// Find ASes that are members of these IXPs.
MATCH (as:AS)-[:MEMBER_OF]->(ixp)

// Count the entities.
RETURN c.name AS country,
       count(DISTINCT ixp) AS numberOfIXPs,
       count(DISTINCT as) AS numberOfASMembers
ORDER BY numberOfIXPs DESC
