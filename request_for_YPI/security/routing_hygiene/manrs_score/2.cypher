// Lists ASes validating RPKI Route Origin (the core MANRS routing security action), ranked by importance.

MATCH (c:Country {country_code: $countryCode})
      <-[:COUNTRY]-
      (as:AS)
      -[:CATEGORIZED]->
      (:Tag {label: "Validating RPKI ROV"})

OPTIONAL MATCH (as)-[r:RANK]->(:Ranking {name:'CAIDA ASRank'})
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

WITH
    as,
    collect(DISTINCT n.name)[0] AS asName,
    r['cone:numberAsns'] AS customerConeSize

RETURN
    as.asn AS asn,
    asName,
    customerConeSize

ORDER BY customerConeSize DESC
LIMIT 20;