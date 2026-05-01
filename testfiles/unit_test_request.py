from neo4j import GraphDatabase, exceptions
import logging
import os
import warnings
import time
from pathlib import Path
from typing import Dict, List, Tuple

warnings.filterwarnings("ignore")

# LOCAL TEST SERVER
#URI = "bolt://localhost:7687"
#AUTH = ("neo4j", "password")

# SERVER TEST CANADA
URI = 'neo4j://iyp-bolt.ihr.live:7687'
AUTH = None


TEST_COUNTRY_CODE = "FR"
TEST_DOMAIN_NAME = "gouv.fr"
TEST_HOSTING_ASN = 16276


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def find_cypher_files(base_path: str = ".") -> Dict[str, List[Path]]:
    """
    Traverses the directory tree and groups .cypher files by indicator.
    Returns a dictionary: {indicator_path: [cypher_files]}
    """
    base = Path(base_path)
    indicators = {}
    for cypher_file in base.rglob("*.cypher"):
        indicator_dir = cypher_file.parent
        if list(indicator_dir.glob("*.md")):
            rel_path = str(indicator_dir.relative_to(base))
            if rel_path not in indicators:
                indicators[rel_path] = []
            indicators[rel_path].append(cypher_file)
    for key in indicators:
        indicators[key] = sorted(indicators[key], key=lambda x: x.name)
    return indicators

def load_cypher_query(file_path: Path) -> str:
    """Loads the content of a .cypher file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else None
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return None

def test_query(driver, query: str, query_file: str) -> Tuple[bool, str, int, float]:
    """
    Tests a Cypher query.
    Returns (success, message, result_count, execution_time)
    """
    try:
        params = {}
        
        if "$countryCode" in query:
            params["countryCode"] = TEST_COUNTRY_CODE
        if "$domainName" in query:
            params["domainName"] = TEST_DOMAIN_NAME
        if "$hostingASN" in query:
            params["hostingASN"] = TEST_HOSTING_ASN

        start_time = time.time()
        
        records, summary, keys = driver.execute_query(
            query,
            parameters_=params,
            database_="neo4j"
        )
        
        elapsed_time = time.time() - start_time
        result_count = len(records)
        
        return True, "OK", result_count, elapsed_time
        
    except exceptions.CypherSyntaxError as e:
        return False, "Cypher syntax error", 0, 0.0
    except Exception as e:
        error_msg = str(e)[:150]
        return False, f"Error: {error_msg}", 0, 0.0

def format_indicator_path(path: str) -> Tuple[str, str, str]:
    """Separates the path into pillar / category / indicator."""
    parts = path.split(os.sep)
    pilier = parts[0] if parts else ""
    categorie = parts[1] if len(parts) > 1 else ""
    indicateur = parts[2] if len(parts) > 2 else ""
    return pilier, categorie, indicateur

def main():
    print(f"{Colors.BOLD}{'='*80}\nCypher Queries Test - YPI\n{'='*80}{Colors.RESET}")
    print(f"Test parameters: country='{TEST_COUNTRY_CODE}', domain='{TEST_DOMAIN_NAME}', asn={TEST_HOSTING_ASN}\n")
    
    indicators = find_cypher_files()
    print(f"Found {len(indicators)} indicator(s) with queries.\n")
    
    total_queries, passed_queries, failed_queries, skipped_queries = 0, 0, 0, 0
    
    print(f"{Colors.YELLOW}Connecting to Neo4j...{Colors.RESET}")
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            print(f"{Colors.GREEN}✓ Connection successful{Colors.RESET}\n")
            
            for indicator_path in sorted(indicators.keys()):
                cypher_files = indicators[indicator_path]
                pilier, categorie, indicateur = format_indicator_path(indicator_path)
                
                print(f"{Colors.BOLD}{Colors.BLUE}{pilier}{Colors.RESET} / {Colors.BOLD}{categorie}{Colors.RESET} / {Colors.BOLD}{indicateur}{Colors.RESET}:")
                
                # Loop to test 1.cypher, 2.cypher, etc.
                for i in range(1, 7):  # Assuming max 6 queries per indicator
                    expected_file = next((f for f in cypher_files if f.name == f"{i}.cypher"), None)
                    
                    if expected_file and expected_file.exists():
                        total_queries += 1
                        query_content = load_cypher_query(expected_file)
                        
                        if not query_content:
                            print(f"  cypher{i}: {Colors.YELLOW}SKIP{Colors.RESET} (empty file)")
                            skipped_queries += 1
                            continue
                        
                        success, message, count, exec_time = test_query(driver, query_content, str(expected_file))
                        
                        if success:
                            time_str = f"{exec_time*1000:.0f}ms" if exec_time < 1 else f"{exec_time:.2f}s"
                            print(f"  cypher{i}: {Colors.GREEN}✓ VALIDATED{Colors.RESET} ({count} results in {time_str})")
                            passed_queries += 1
                        else:
                            print(f"  cypher{i}: {Colors.RED}✗ FAILED{Colors.RESET} - {message}")
                            failed_queries += 1

            print(f"{Colors.BOLD}{'='*80}\n{Colors.BOLD}TEST SUMMARY\n{'='*80}{Colors.RESET}")
            print(f"Total queries tested:       {total_queries}")
            print(f"{Colors.GREEN}✓ Passed:                   {passed_queries}{Colors.RESET}")
            print(f"{Colors.RED}✗ Failed:                   {failed_queries}{Colors.RESET}")
            print(f"{Colors.YELLOW}⊘ Skipped (empty):          {skipped_queries}{Colors.RESET}")
            
            tests_executed = passed_queries + failed_queries
            if tests_executed > 0:
                success_rate = (passed_queries / tests_executed) * 100
                print(f"\n{Colors.BOLD}Success rate: {success_rate:.1f}%{Colors.RESET} ({passed_queries}/{tests_executed} queries)")
            else:
                print(f"\n{Colors.YELLOW}No queries tested{Colors.RESET}")
            
    except exceptions.ServiceUnavailable:
        print(f"{Colors.RED}✗ Error: Unable to connect to Neo4j{Colors.RESET}")
    except exceptions.AuthError:
        print(f"{Colors.RED}✗ Authentication error{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Unexpected error: {e}{Colors.RESET}")

if __name__ == "__main__":
    logging.getLogger("neo4j").setLevel(logging.ERROR)
    main()