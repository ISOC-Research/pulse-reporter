from neo4j import GraphDatabase
URI = 'neo4j://iyp-bolt.ihr.live:7687'
driver = GraphDatabase.driver(URI, auth=None)

# Current outputs for AU
q1 = "MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'}) RETURN count(DISTINCT a) AS total"
q2 = "MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'}) MATCH (a)-[:LOCATED_IN]->(f:Facility) RETURN count(DISTINCT f) AS total"
q3 = "MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'}) MATCH (a)-[:LOCATED_IN]->(p:Point) RETURN count(DISTINCT p) AS total"
q4 = "MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'}) MATCH (a)-[:PEERS_WITH]-(b:AS) RETURN count(DISTINCT b) AS total"

for label, q in [("Q1 AS count", q1), ("Q2 Facility count", q2), ("Q3 Point count", q3), ("Q4 Peering count", q4)]:
    records, _, _ = driver.execute_query(q, database_='neo4j')
    print(label + ":", records[0]["total"])

print()

# Q1: How many are active (originate BGP)?
q1b = """
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'})
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)
WITH a, count(pfx) AS pfxCount
RETURN count(CASE WHEN pfxCount > 0 THEN 1 END) AS Active,
       count(CASE WHEN pfxCount = 0 THEN 1 END) AS Dormant
"""
records, _, _ = driver.execute_query(q1b, database_='neo4j')
print("Q1 breakdown - Active vs Dormant ASes:")
for r in records:
    print("  Active:", r["Active"], "| Dormant:", r["Dormant"])

# Q2: Facility query doesn't filter by country on the facility side
# Are there cases where an AU AS is LOCATED_IN a non-AU facility?
q2b = """
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'})
MATCH (a)-[:LOCATED_IN]->(f:Facility)
OPTIONAL MATCH (f)-[:COUNTRY]->(fc:Country)
WITH f, fc.country_code AS fcc
RETURN fcc, count(DISTINCT f) AS facilities
ORDER BY facilities DESC
LIMIT 10
"""
records, _, _ = driver.execute_query(q2b, database_='neo4j')
print()
print("Q2: Facilities of AU ASes broken down by facility country:")
for r in records:
    print("  " + str(r["fcc"]) + ": " + str(r["facilities"]) + " facilities")

# Q4: Peering query counts ALL peers globally. How many are domestic vs foreign?
q4b = """
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'})
MATCH (a)-[:PEERS_WITH]-(b:AS)
OPTIONAL MATCH (b)-[:COUNTRY]->(bc:Country)
WITH b, COLLECT(DISTINCT bc.country_code) AS peer_countries
RETURN
  count(DISTINCT CASE WHEN 'AU' IN peer_countries THEN b END) AS DomesticPeers,
  count(DISTINCT CASE WHEN NOT 'AU' IN peer_countries THEN b END) AS ForeignPeers
"""
records, _, _ = driver.execute_query(q4b, database_='neo4j')
print()
print("Q4: Peering breakdown - domestic vs foreign:")
for r in records:
    print("  Domestic peers:", r["DomesticPeers"], "| Foreign peers:", r["ForeignPeers"])

# What about IXP membership count? Critical for network coverage.
q5 = """
MATCH (a:AS)-[:COUNTRY]->(c:Country {country_code: 'AU'})
WHERE (a)-[:ORIGINATE]->()
OPTIONAL MATCH (a)-[:MEMBER_OF]->(i:IXP)-[:COUNTRY]->(c)
WITH a, count(DISTINCT i) AS ixpCount
RETURN count(CASE WHEN ixpCount > 0 THEN 1 END) AS IXPConnected,
       count(CASE WHEN ixpCount = 0 THEN 1 END) AS NotIXPConnected
"""
records, _, _ = driver.execute_query(q5, database_='neo4j')
print()
print("Active ASes with vs without local IXP membership:")
for r in records:
    print("  IXP Connected:", r["IXPConnected"], "| Not Connected:", r["NotIXPConnected"])

driver.close()
