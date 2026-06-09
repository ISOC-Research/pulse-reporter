MATCH ()-[r]->()
RETURN
type(r) AS domainName,
0.0 AS queryPercentage