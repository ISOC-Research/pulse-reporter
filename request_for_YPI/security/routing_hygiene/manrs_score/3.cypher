// Breaks down routing hygiene actions (RPKI + IRR tags) implemented by ASes in a country.
// RPKI Valid/IRR Valid correspond to MANRS-recommended origin validation and route filtering actions.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)-[:CATEGORIZED]->(t:Tag)
WHERE t.label IN ['RPKI Valid', 'RPKI Invalid', 'RPKI NotFound', 'IRR Valid', 'IRR Invalid', 'IRR NotFound',
                  'Validating RPKI ROV', 'Not Validating RPKI ROV']

WITH t.label AS routingHygieneAction, count(DISTINCT as) AS implementingASNs

RETURN
  routingHygieneAction,
  implementingASNs
ORDER BY implementingASNs DESC;