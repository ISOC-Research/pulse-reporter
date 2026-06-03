// Lists Content Delivery Network (CDN) ASes located in the target country.
// Uses the "Content Delivery Network" tag from the IYP dataset.
//
// Problem solved:
// An AS can have multiple Name nodes attached (e.g. OVH, OVHcloud, OVH SAS),
// which previously caused duplicate rows in the output.
// We use collect(DISTINCT n.name)[0] to select a single representative name
// for each ASN and avoid duplicates.
//
// The parameter $countryCode must be provided during execution
// (e.g., 'FR', 'SN', 'JP').

// Step 1: Find all ASes belonging to the target country.
MATCH (c:Country {country_code: $countryCode})<-[:COUNTRY]-(as:AS)

// Step 2: Keep only ASes tagged as Content Delivery Networks (CDNs).
MATCH (as)-[:CATEGORIZED]->(:Tag {label: 'Content Delivery Network'})

// Step 3: Retrieve AS names.
// OPTIONAL MATCH is used because some ASes may not have a Name node.
OPTIONAL MATCH (as)-[:NAME]->(n:Name)

// Step 4: Group results by ASN and collect all attached names.
// DISTINCT prevents duplicate names.
// [0] selects the first available name as the representative display name.
WITH as,
     collect(DISTINCT n.name)[0] AS cdnName

// Step 5: Return one row per CDN ASN.
RETURN
       as.asn AS cdnASN,
       cdnName

// Step 6: Sort alphabetically by CDN name.
ORDER BY cdnName;