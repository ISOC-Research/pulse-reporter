// MANRS Action 3: Coordination — measures PeeringDB network registration rate.
// PeeringDB registration is the primary evidence of MANRS Action 3 compliance:
// operators must publish accurate contact and routing policy information so that
// peers can coordinate during routing incidents. An AS with a PeeringDB entry
// is reachable, documented, and demonstrably open to coordination.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
WITH count(DISTINCT as) AS totalASNs

MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(pdbAS:AS)-[:EXTERNAL_ID]->(:PeeringdbNetID)
WITH totalASNs, count(DISTINCT pdbAS) AS peeringdbCount

RETURN
  totalASNs,
  peeringdbCount,
  round(100.0 * peeringdbCount / totalASNs, 2) AS coordinationRatePercentage;
