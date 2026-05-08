import os
import glob
from neo4j import GraphDatabase

URI = 'neo4j://iyp-bolt.ihr.live:7687'
PARAMS = {"countryCode": "AU", "domainName": "gouv.fr", "hostingASN": 16276}

def test_all():
    base_dir = "request_for_YPI"
    cypher_files = glob.glob(f"{base_dir}/**/*.cypher", recursive=True)
    
    results = {"working": [], "empty": [], "error": []}
    
    with GraphDatabase.driver(URI, auth=None) as driver:
        with driver.session(database='neo4j') as session:
            for file_path in sorted(cypher_files):
                indicator_name = os.path.basename(os.path.dirname(file_path))
                query_name = f"{indicator_name}/{os.path.basename(file_path)}"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    query = f.read()
                
                try:
                    # Execute with short timeout so it doesn't hang
                    tx = session.begin_transaction(timeout=3.0)
                    records = tx.run(query, PARAMS).data()
                    tx.commit()
                    
                    if len(records) > 0:
                        results["working"].append(query_name)
                    else:
                        results["empty"].append(query_name)
                except Exception as e:
                    if 'tx' in locals():
                        try:
                            tx.rollback()
                        except:
                            pass
                    results["error"].append((query_name, str(e).splitlines()[0]))

    print("=== FINAL RESULTS ===")
    print(f"\n[WORKING] ({len(results['working'])} queries):")
    for q in results["working"]:
        print(f"  - {q}")
        
    print(f"\n[EMPTY] ({len(results['empty'])} queries):")
    for q in results["empty"]:
        print(f"  - {q}")
        
    print(f"\n[ERROR] ({len(results['error'])} queries):")
    for q, err in results["error"]:
        print(f"  - {q}: {err}")

if __name__ == "__main__":
    test_all()
