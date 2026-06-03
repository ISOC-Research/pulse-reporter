// Routing hygiene breakdown based on prefixes originated by ASes in the country.
// Measures RPKI and IRR status of announced prefixes.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').

MATCH (c:Country {country_code: $countryCode})
      <-[:COUNTRY]-
      (as:AS)
      -[:ORIGINATE]->
      (p:BGPPrefix)

MATCH (p)-[:CATEGORIZED]->(t:Tag)

WHERE t.label IN [
    'RPKI Valid',
    'RPKI Invalid',
    'RPKI NotFound',
    'IRR Valid',
    'IRR Invalid',
    'IRR NotFound'
]

RETURN
    t.label AS routingHygieneAction,
    count(DISTINCT p) AS implementingASNs
ORDER BY implementingASNs DESC;