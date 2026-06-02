from neo4j import GraphDatabase
URI = 'neo4j://iyp-bolt.ihr.live:7687'
driver = GraphDatabase.driver(URI, auth=None)

# Fix: collect IXPs per AS instead of one row per IXP
q = """
MATCH (i:IXP)-[:COUNTRY]->(ic:Country {country_code: 'AU'})
MATCH (i)<-[:MEMBER_OF]-(a:AS)
OPTIONAL MATCH (a)-[:COUNTRY]->(ac:Country)
WITH i, a, COLLECT(DISTINCT ac.country_code) AS member_countries
WHERE NOT 'AU' IN member_countries
OPTIONAL MATCH (a)-[rel:RANK]->(r:Ranking {name: 'CAIDA ASRank'})
OPTIONAL MATCH (a)-[:NAME]->(n:Name)
WITH a.asn AS ASN, MIN(n.name) AS NetworkName, COLLECT(DISTINCT i.name) AS IXPs, MIN(rel.rank) AS CaidaRank
WHERE CaidaRank IS NOT NULL
RETURN ASN, NetworkName, IXPs, CaidaRank
ORDER BY CaidaRank ASC
LIMIT 15
"""
records, _, _ = driver.execute_query(q, database_='neo4j')
print("Total:", len(records))
for r in records:
    print("AS" + str(r["ASN"]) + " | " + str(r["NetworkName"]) + " | rank #" + str(r["CaidaRank"]) + " | IXPs: " + str(r["IXPs"]))

driver.close()
