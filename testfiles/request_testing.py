import sys
import argparse
from neo4j import GraphDatabase, exceptions

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
    """
    Loads a Cypher query from a specified file.
    In case of error (file not found, etc.), the script stops.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f"✅ File '{file_path}' successfully read.")
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main script function.
    """
    parser = argparse.ArgumentParser(
        description="Executes a Cypher query from a file on a Neo4j database."
    )
    parser.add_argument(
        "file_path", 
        help="The path to the .cypher file containing the query."
    )
    
    # --- MODIFICATION HERE : Added 'default' parameter ---
    parser.add_argument(
        "--country", 
        default=DEFAULT_COUNTRY,
        help=f"Value for the $countryCode parameter (default: {DEFAULT_COUNTRY})"
    )
    parser.add_argument(
        "--domain", 
        default=DEFAULT_DOMAIN,
        help=f"Value for the $domainName parameter (default: {DEFAULT_DOMAIN})"
    )
    parser.add_argument(
        "--asn", 
        type=int, 
        default=DEFAULT_ASN,
        help=f"Value for the $hostingASN parameter (default: {DEFAULT_ASN})"
    )

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
            print("✔️ Connection successful !")

            print("\n🚀 Executing query...")
            records, summary, _ = driver.execute_query(
                cypher_query,
                parameters_=params,
                database_="neo4j"
            )

            print("\n" + "="*30)
            print(f"📊 RESULTS ({len(records)} records)")
            print("="*30)

            if not records:
                print("The query returned no results.")
            else:
                for i, record in enumerate(records):
                    print(f"--- Record #{i + 1} ---")
                    for key, value in record.data().items():
                        print(f"  - {key}: {value}")
                print("##################")
                print(records)

            print("\n" + "="*30)
            print("📝 EXECUTION SUMMARY")
            print("="*30)
            print(f"Query executed in: {summary.result_available_after} ms")
            print(f"Target database: '{summary.database}'")

    except exceptions.ServiceUnavailable:
        print(f"\n❌ Error: Unable to connect to Neo4j at {URI}.", file=sys.stderr)
        sys.exit(1)
    except exceptions.AuthError:
        print("\n❌ Error: Authentication denied. Check your credentials.", file=sys.stderr)
        sys.exit(1)
    except exceptions.CypherSyntaxError as e:
        print(f"\n❌ Cypher syntax error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()