// Lists ASes validating RPKI Route Origin (the core MANRS routing security action), ranked by importance.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:CATEGORIZED]->(t:Tag {label: "Validating RPKI ROV"})

// Optional join with the CAIDA ranking to get the customer cone size.
OPTIONAL MATCH (as)-[r:RANK]->(rk:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

RETURN
  as.asn AS asn,
  n.name AS asName,
  r['cone:numberAsns'] AS customerConeSize
ORDER BY customerConeSize DESC
LIMIT 20;