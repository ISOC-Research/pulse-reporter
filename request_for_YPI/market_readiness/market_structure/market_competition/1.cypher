// Récupère la part de marché de chaque AS dans un pays donné.
// Le paramètre $countryCode doit être fourni lors de l'exécution (ex: 'CI' pour la Côte d'Ivoire).
MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)
// Récupère le nom de l'AS pour une meilleure lisibilité.
OPTIONAL MATCH (as)-[:NAME]->(n:Name)
WITH as, p, collect(DISTINCT n.name)[0] AS asName
RETURN as.asn AS asn,
       asName,
       p.percent AS marketSharePercent
ORDER BY marketSharePercent DESC
LIMIT 30;