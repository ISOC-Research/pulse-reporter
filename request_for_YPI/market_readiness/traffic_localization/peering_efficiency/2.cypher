// Lists domestic IXPs and their number of local AS members.
// The $countryCode parameter must be provided during execution (e.g., 'KE', 'NG', 'US').
MATCH (c:Country {country_code: $countryCode})
MATCH (ixp:IXP)-[:COUNTRY]->(c)
MATCH (local_as:AS)-[:COUNTRY]->(c)
MATCH (local_as)-[:MEMBER_OF]->(ixp)
RETURN id(ixp) AS ixpId,
       ixp.name AS ixpName,
       count(DISTINCT local_as) AS localMemberCount
ORDER BY localMemberCount DESC
LIMIT 15;