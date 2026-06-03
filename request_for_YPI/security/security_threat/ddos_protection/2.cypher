// Measures the percentage of the country's population served by CDN ASes.
// The parameter $countryCode must be provided (e.g., 'FR', 'SN', 'JP').

MATCH (c:Country {country_code: $countryCode})<-[p:POPULATION]-(as:AS)

MATCH (as)-[:CATEGORIZED]->(:Tag {label: 'Content Delivery Network'})

OPTIONAL MATCH (as)-[:NAME]->(n:Name)

// Collapse multiple Name nodes into a single representative name
WITH as,
     p.percent AS populationServedPercentage,
     collect(DISTINCT n.name)[0] AS cdnName

RETURN
       as.asn AS cdnASN,
       cdnName,
       populationServedPercentage

ORDER BY populationServedPercentage DESC;