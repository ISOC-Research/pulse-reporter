MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)
MATCH (as)-[:ORIGINATE]->(p:BGPPrefix)
WITH c, count(p) AS total, count(CASE WHEN p.af = 6 THEN p ELSE null END) AS ipv6
RETURN (toFloat(ipv6) / total) * 100.0 AS percentage