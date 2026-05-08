// MANRS Action 1: Route Filtering — measures the IRR Valid route registration rate.
// IRR (Internet Routing Registry) registration is the technical prerequisite for
// route filtering, which is MANRS Action 1. An operator with IRR-valid prefixes has
// registered its route announcements, enabling peers to filter based on authoritative data.
// Note: IRR Valid is a tag on BGPPrefix nodes (not AS nodes directly).
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNs

// Count ASes that have at least one IRR-valid BGP prefix.
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(irrAS:AS)-[:ORIGINATE]->(p:BGPPrefix)-[:CATEGORIZED]->(t:Tag {label: "IRR Valid"})
WITH totalASNs, count(DISTINCT irrAS) AS irrValidCount

RETURN
  totalASNs,
  irrValidCount,
  round(100.0 * irrValidCount / totalASNs, 2) AS irrValidRatePercentage;
