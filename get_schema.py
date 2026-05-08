from neo4j import GraphDatabase

URI = 'neo4j://iyp-bolt.ihr.live:7687'

def get_schema():
    with GraphDatabase.driver(URI, auth=None) as driver:
        with driver.session(database='neo4j') as session:
            labels_result = session.run("CALL db.labels()").data()
            rels_result = session.run("CALL db.relationshipTypes()").data()
            
            labels = [record['label'] for record in labels_result]
            rels = [record['relationshipType'] for record in rels_result]
            
            print("=== LABELS ===")
            for l in sorted(labels):
                print(l)
                
            print("\n=== RELATIONSHIPS ===")
            for r in sorted(rels):
                print(r)

if __name__ == "__main__":
    get_schema()
