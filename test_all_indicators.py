import os
import glob
from neo4j import GraphDatabase

URI = 'neo4j://iyp-bolt.ihr.live:7687'
PARAMS = {"countryCode": "FR", "domainName": "gouv.fr", "hostingASN": 16276}

base_dir = "request_for_YPI"
cypher_files = glob.glob(f"{base_dir}/**/*.cypher", recursive=True)

results = {"working": [], "empty": [], "error": []}

print("=== STARTING CROSS-REFERENCE ===")

with GraphDatabase.driver(URI, auth=None) as driver:
    for file_path in sorted(cypher_files):
        indicator_name = os.path.basename(os.path.dirname(file_path))
        query_name = f"{indicator_name}/{os.path.basename(file_path)}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                query = f.read()
            
            # Using transaction with timeout to avoid hanging on heavy queries
            with driver.session(database='neo4j') as session:
                records = session.run(query, PARAMS, timeout=5.0).data()
            
            if len(records) > 0:
                print(f"[WORKING] {query_name} ({len(records)} records)")
                results["working"].append(query_name)
            else:
                print(f"[EMPTY]   {query_name}")
                results["empty"].append(query_name)
                
        except Exception as e:
            err_msg = str(e).splitlines()[0] if str(e) else type(e).__name__
            print(f"[ERROR]   {query_name} -> {err_msg}")
            results["error"].append((query_name, err_msg))

print("\n=== FINAL SUMMARY ===")
print(f"Working: {len(results['working'])}")
print(f"Empty:   {len(results['empty'])}")
print(f"Errors:  {len(results['error'])}")
