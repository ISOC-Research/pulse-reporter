MATCH (c:Country {country_code: $countryCode})<-[pop:POPULATION]-(as:AS)

OPTIONAL MATCH (as)-[:NAME]->(n:Name)

OPTIONAL MATCH (as)-[:CATEGORIZED]->(rpkiTag:Tag {label: "Validating RPKI ROV"})

WITH
    as,
    pop.percent AS populationServedPercentage,
    collect(DISTINCT n.name)[0] AS name,
    count(rpkiTag) > 0 AS isRpkiValidating

RETURN
    as.asn AS asn,
    name,
    populationServedPercentage,
    isRpkiValidating

ORDER BY populationServedPercentage DESC
LIMIT 10