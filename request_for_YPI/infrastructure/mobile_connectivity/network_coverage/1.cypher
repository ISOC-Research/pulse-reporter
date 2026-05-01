// Network coverage: number of ASes registered in the country.

MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: $countryCode})
RETURN c.name AS Country,
       COUNT(DISTINCT a) AS ASN_Count;

