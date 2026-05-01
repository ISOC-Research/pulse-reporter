// Finds the highest-ranked international networks present on the IXPs of a country.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (i:IXP)<-[:MEMBER_OF]-(a:AS)-[:COUNTRY]->(c:Country)
WHERE c.country_code <> $countryCode
AND EXISTS {
    MATCH (a2:AS)-[:COUNTRY]->(c2:Country {country_code: $countryCode})
    MATCH (a2)-[:MEMBER_OF]->(i)
}
OPTIONAL MATCH (a)-[:RANK]->(r:Ranking)
RETURN a.asn AS ASN, i.name AS IXP, r.name AS Rank
ORDER BY r.name ASC
LIMIT 10;