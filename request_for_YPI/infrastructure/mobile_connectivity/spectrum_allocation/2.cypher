// Top network operators by BGP prefix count — largest IP address space holders,
// broken down by IPv4/IPv6 with adoption readiness flag.
// The $countryCode parameter must be provided during execution (e.g., 'AU', 'FR', 'DE').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a, MIN(n.name) AS OperatorName,
     COUNT(DISTINCT CASE WHEN p.af = 4 THEN p END) AS IPv4Prefixes,
     COUNT(DISTINCT CASE WHEN p.af = 6 THEN p END) AS IPv6Prefixes
WITH a.asn AS ASN, OperatorName, IPv4Prefixes, IPv6Prefixes,
     (IPv4Prefixes + IPv6Prefixes) AS TotalPrefixes,
     CASE WHEN IPv6Prefixes > 0 THEN 'Yes' ELSE 'No' END AS IPv6Adopted
RETURN ASN, OperatorName, TotalPrefixes, IPv4Prefixes, IPv6Prefixes, IPv6Adopted
ORDER BY TotalPrefixes DESC
LIMIT 20;
