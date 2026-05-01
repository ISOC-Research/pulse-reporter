import sys
import os
import argparse
from neo4j import GraphDatabase, exceptions

# 1. Get the main project folder
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# 2. Add the request_for_YPI folder so Python can find "src" globally
request_for_ypi_dir = os.path.join(root_dir, 'request_for_YPI')
sys.path.append(request_for_ypi_dir)

from request_for_YPI.src.utils.formatting import format_neo4j_results
# ==========================================================
#  NEO4J CONNECTION CONFIGURATION
# ==========================================================
# LOCAL TEST SERVER
#URI = "bolt://localhost:7687"
#AUTH = ("neo4j", "password")

# SERVER TEST CANADA
URI = 'neo4j://iyp-bolt.ihr.live:7687'
AUTH = None
# ==========================================================

# ==========================================================
#  DEFAULT PARAMETERS FOR QUERIES
# ==========================================================
DEFAULT_COUNTRY = "FR"
DEFAULT_DOMAIN = "gouv.fr"
DEFAULT_ASN = 16276
# ==========================================================

def load_query_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Executes a Cypher query and formats the result for an LLM."
    )
    parser.add_argument("file_path", help="The path to the .cypher file containing the query.")
    parser.add_argument("--country", default=DEFAULT_COUNTRY, help=f"Country code (default: {DEFAULT_COUNTRY})")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help=f"Domain name (default: {DEFAULT_DOMAIN})")
    parser.add_argument("--asn", type=int, default=DEFAULT_ASN, help=f"AS Number (default: {DEFAULT_ASN})")
    args = parser.parse_args()

    cypher_query = load_query_from_file(args.file_path)
    
    params = {
        "countryCode": args.country,
        "domainName": args.domain,
        "hostingASN": args.asn
    }

    print(f"⚙️  Parameters used: {params}")

    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            print("⚡️ Connecting to Neo4j database...")
            driver.verify_connectivity()
            
            print("🚀 Executing query...")
            records, summary, _ = driver.execute_query(
                cypher_query,
                parameters_=params,
                database_="neo4j"
            )

            print("\n" + "="*50)
            print("✅ RAW RESULT RECEIVED FROM NEO4J")
            print("="*50)
            print(f"{len(records)} record(s) found.")

            print("\n" + "="*50)
            print("✨ RESULT FORMATTED FOR THE LLM (via query_templates.yaml)")
            print("="*50)
            

            formatted_text = format_neo4j_results(
                query_path=args.file_path,
                records=records,
                params=params
            )
    
            print(formatted_text)



    except exceptions.ServiceUnavailable:
        print(f"\n❌ Error: Unable to connect to Neo4j at {URI}.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()