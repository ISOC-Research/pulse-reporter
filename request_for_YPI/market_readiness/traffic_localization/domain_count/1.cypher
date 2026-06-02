// Identifies the ccTLD domains most frequently queried from within the country.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})
// Filters domains that end with the country's ccTLD (e.g., .sn)
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Finds the query relationship from this country (source: Cloudflare Radar)
MATCH (d)-[q:QUERIED_FROM]->(c)
WHERE q.value IS NOT NULL

RETURN d.name AS localDomain,
       q.value AS percentageOfQueriesInCountry
ORDER BY percentageOfQueriesInCountry DESC
LIMIT 20;