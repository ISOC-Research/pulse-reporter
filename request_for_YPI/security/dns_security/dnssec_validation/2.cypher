// Identifies the largest access networks (by population) and checks their RPKI ROV validation status.
// RPKI ROV validation is the core routing security action promoted by MANRS.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'DE', 'BR').
MATCH (c:Country {country_code: $countryCode})<-[pop:POPULATION]-(as:AS)
// Retrieves the AS name.
OPTIONAL MATCH (as)-[:NAME]->(n:Name)
// Checks if the AS is validating RPKI Route Origins.
OPTIONAL MATCH (as)-[:CATEGORIZED]->(rpkiTag:Tag {label: "Validating RPKI ROV"})
RETURN
    as.asn AS asn,
    n.name AS name,
    pop.percent AS populationServedPercentage,
    (rpkiTag IS NOT NULL) AS isRpkiValidating
ORDER BY populationServedPercentage DESC
LIMIT 10;