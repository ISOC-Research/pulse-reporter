import os
import glob
from neo4j import GraphDatabase

URI = 'neo4j://iyp-bolt.ihr.live:7687'
PARAMS = {"countryCode": "AU", "domainName": "gouv.fr", "hostingASN": 16276}

base_dir = "request_for_YPI"
cypher_files = glob.glob(f"{base_dir}/**/*.cypher", recursive=True)

print("Testing all queries against Neo4j...")

with GraphDatabase.driver(URI, auth=None) as driver:
    for file_path in sorted(cypher_files):
        query_name = "/".join(file_path.split(os.sep)[-3:])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                query = f.read()
            
            with driver.session(database='neo4j') as session:
                # We do a quick run
                records = session.run(query, PARAMS).data()
            
            if len(records) > 0:
                print(f"[WORKING] {query_name} ({len(records)} records)")
            else:
                print(f"[EMPTY]   {query_name}")
                
        except Exception as e:
            print(f"[ERROR]   {query_name} -> {e}")
