// Measures the depth of IXP peering — how many IXPs each local AS participates in.
// An AS peering at multiple IXPs has better redundancy and resilience.
// The $countryCode parameter must be provided at execution.
MATCH (c:Country {country_code: $countryCode})
MATCH (as:AS)-[:COUNTRY]->(c)

// Find all local IXPs the AS is a member of.
OPTIONAL MATCH (ixp:IXP)-[:COUNTRY]->(c)
OPTIONAL MATCH (as)-[:MEMBER_OF]->(ixp)

WITH as, count(DISTINCT ixp) AS ixpMembershipCount
WHERE ixpMembershipCount > 0

// Group by membership count to show the distribution.
RETURN
    ixpMembershipCount AS numberOfIXPsMemberOf,
    count(DISTINCT as) AS numberOfASes
ORDER BY ixpMembershipCount DESC;