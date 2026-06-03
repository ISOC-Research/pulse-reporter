MATCH (c:Country {country_code: $countryCode})
MATCH (c)<-[:COUNTRY]-(a:AS)-[:ORIGINATE]->(p:BGPPrefix)

WITH c, count(DISTINCT p) AS totalPrefixes

MATCH (c)<-[:COUNTRY]-(a2:AS)
MATCH (a2)-[:ROUTE_ORIGIN_AUTHORIZATION]->(rp:RPKIPrefix)
MATCH (rp)-[:PART_OF]->(p2:BGPPrefix)

WITH c,
     totalPrefixes,
     count(DISTINCT p2) AS coveredPrefixes

RETURN
       c.name AS country,
       totalPrefixes,
       coveredPrefixes,
       round(
           (toFloat(coveredPrefixes) / totalPrefixes) * 100.0,
           2
       ) AS rpkiCoveragePercentage;