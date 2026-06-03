// Mesure la dépendance moyenne des AS d'un pays envers leurs fournisseurs de transit.
// The $countryCode parameter must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)
// Utilise la relation de dépendance et la métrique d'hégémonie de l'IHR.
MATCH (as)-[d:DEPENDS_ON]->(provider:AS)
// Filtre pour les dépendances significatives afin de réduire le bruit.
WHERE d.hege > 0.1 AND NOT (provider)-[:COUNTRY]->(c)
WITH provider, avg(d.hege) AS averageHegemony, count(DISTINCT as) AS dependentASNs
OPTIONAL MATCH (provider)-[:NAME]->(n:Name)
WITH provider, averageHegemony, dependentASNs, collect(DISTINCT n.name)[0] AS providerName
RETURN provider.asn AS providerASN,
       providerName,
       averageHegemony,
       dependentASNs
ORDER BY dependentASNs DESC, averageHegemony DESC
LIMIT 50;