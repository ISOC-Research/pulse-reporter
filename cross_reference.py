import os
import glob
import re
from neo4j import GraphDatabase

URI = 'neo4j://iyp-bolt.ihr.live:7687'

def check_indicators():
    with GraphDatabase.driver(URI, auth=None) as driver:
        with driver.session(database='neo4j') as session:
            labels_result = session.run("CALL db.labels()").data()
            rels_result = session.run("CALL db.relationshipTypes()").data()
            
            db_labels = set([record['label'] for record in labels_result])
            db_rels = set([record['relationshipType'] for record in rels_result])

    base_dir = "request_for_YPI"
    cypher_files = glob.glob(f"{base_dir}/**/*.cypher", recursive=True)
    
    results = {}
    
    for file_path in cypher_files:
        indicator_name = os.path.basename(os.path.dirname(file_path))
        query_name = f"{indicator_name}/{os.path.basename(file_path)}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            query = f.read()
            
        # Extract labels: pattern (:Label)
        labels = set(re.findall(r'\(([a-zA-Z0-9_]*):([A-Za-z0-9_]+)', query))
        # this returns a list of tuples (var, label). We just want the label
        node_labels = set([x[1] for x in labels])
        
        # Extract relationships: pattern [:REL] or [r:REL]
        rels = set(re.findall(r'\[([a-zA-Z0-9_]*):([A-Za-z0-9_]+)', query))
        rel_types = set([x[1] for x in rels])
        
        missing_labels = [l for l in node_labels if l not in db_labels]
        missing_rels = [r for r in rel_types if r not in db_rels]
        
        # Explicit properties/tags that we know might be missing
        tags = set()
        if 'label: \'CDN\'' in query or 'label:"CDN"' in query:
            tags.add('Tag: CDN')
        if 'name:"MANRS"' in query.replace(" ", ""):
            tags.add('Organization: MANRS')
            
        results[query_name] = {
            'missing_labels': missing_labels,
            'missing_rels': missing_rels,
            'tags': tags,
            'query': query
        }
        
    print("=== CROSS REFERENCE RESULTS ===")
    for query_name, data in sorted(results.items()):
        if data['missing_labels'] or data['missing_rels'] or data['tags']:
            print(f"\n[BROKEN SCHEMA] {query_name}")
            if data['missing_labels']:
                print(f"  Missing Nodes: {', '.join(data['missing_labels'])}")
            if data['missing_rels']:
                print(f"  Missing Relationships: {', '.join(data['missing_rels'])}")
            if data['tags']:
                print(f"  Missing Data Properties: {', '.join(data['tags'])}")
        else:
            pass # print(f"[OK] {query_name}")

if __name__ == "__main__":
    check_indicators()
