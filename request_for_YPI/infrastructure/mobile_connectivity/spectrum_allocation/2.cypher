// Top 10 ASes by number of BGP prefixes announced — identifies operators with the
// largest IP address space allocations, a proxy for the largest network capacity holders.
// The parameter $countryCode must be provided during execution (e.g., 'FR', 'SN', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:ORIGINATE]->(p:BGPPrefix)
OPTIONAL MATCH (as)-[:NAME]->(n:Name)
WITH as, n,
     count(DISTINCT CASE WHEN p.af = 4 THEN p ELSE null END) AS ipv4Count,
     count(DISTINCT CASE WHEN p.af = 6 THEN p ELSE null END) AS ipv6Count
WITH as, n, ipv4Count, ipv6Count, (ipv4Count + ipv6Count) AS totalPrefixes
WHERE totalPrefixes > 0
RETURN as.asn       AS ASN,
       n.name       AS operatorName,
       totalPrefixes AS totalPrefixes,
       ipv4Count    AS ipv4Prefixes,
       ipv6Count    AS ipv6Prefixes
ORDER BY totalPrefixes DESC
LIMIT 10;
