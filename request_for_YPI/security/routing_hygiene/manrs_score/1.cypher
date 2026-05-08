// Calculates the RPKI Route Origin Validation (ROV) adoption rate for a country.
// This is the primary technical action promoted by MANRS (routing security best practices).
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNsInCountry

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(rpkiAS:AS)-[:CATEGORIZED]->(t:Tag {label: "Validating RPKI ROV"})
WITH totalASNsInCountry, count(DISTINCT rpkiAS) AS rpkiValidatingCount

RETURN
  totalASNsInCountry,
  rpkiValidatingCount,
  round(100.0 * rpkiValidatingCount / totalASNsInCountry, 2) AS adoptionRatePercentage;