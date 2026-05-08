// Calculates the RPKI Route Origin Validation (ROV) adoption rate as a routing hygiene proxy.
// Used here to contextualize DNSSEC validation: networks that validate routing origins
// are more likely to be operating secure, well-managed DNS infrastructure.
// The parameter $countryCode must be provided during execution (e.g., 'KE', 'DE', 'BR').
MATCH (c:Country {country_code: $countryCode})
// Counts the total number of ASes in the country.
OPTIONAL MATCH (as:AS)-[:COUNTRY]->(c)
WITH c, count(DISTINCT as) AS totalASNs
// Counts ASes that validate RPKI Route Origin (MANRS-equivalent proxy).
OPTIONAL MATCH (rpki_as:AS)-[:COUNTRY]->(c)
WHERE (rpki_as)-[:CATEGORIZED]->(:Tag {label: "Validating RPKI ROV"})
WITH totalASNs, count(DISTINCT rpki_as) AS rpkiValidatingASNs
RETURN
    rpkiValidatingASNs,
    totalASNs,
    CASE
        WHEN totalASNs > 0 THEN (toFloat(rpkiValidatingASNs) / totalASNs) * 100
        ELSE 0
    END AS rpkiValidationPercentage;