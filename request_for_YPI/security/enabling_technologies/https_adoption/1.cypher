MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)
MATCH (as)-[:HAS_HTTPS]->(h:HTTPSStatus)
WITH count(as) AS total, count(CASE WHEN h.status = 'enabled' THEN as ELSE null END) AS enabled
RETURN CASE WHEN total = 0 THEN 0 ELSE (toFloat(enabled) / total) * 100.0 END AS percentage