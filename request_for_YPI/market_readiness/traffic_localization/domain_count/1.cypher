// Identifie les domaines du ccTLD les plus requêtés depuis l'intérieur du pays.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})
// Filtre les domaines qui se terminent par le ccTLD du pays (ex: .sn)
MATCH (d:DomainName)
WHERE d.name ENDS WITH '.' + toLower($countryCode)

// Trouve la relation de requête depuis ce pays (source: Cloudflare Radar)
MATCH (d)-[q:QUERIED_FROM]->(c)
WHERE q.value IS NOT NULL

RETURN d.name AS localDomain,
       q.value AS percentageOfQueriesInCountry
ORDER BY percentageOfQueriesInCountry DESC
LIMIT 20;