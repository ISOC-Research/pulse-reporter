import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from request_for_YPI.src.request_IYP.request_testing import execute_cypher_test

COUNTRY = "IN"

query = f"""
MATCH (i:IXP)-[:COUNTRY]->(c:Country {{country_code: '{COUNTRY}'}})
OPTIONAL MATCH (i)-[:LOCATED_IN]->(f:Facility)

RETURN
    i.name AS IXP,
    COLLECT(DISTINCT f.name) AS Facilities
ORDER BY IXP
"""

result = execute_cypher_test(query)

print("=" * 70)
print("INDIA IXP DISCOVERY")
print("=" * 70)

if not result["success"]:
    print("ERROR:")
    print(result["error"])
else:
    print(f"IXPs found: {len(result['data'])}")
    print()

    for row in result["data"]:
        print(f"IXP: {row['IXP']}")
        print(f"Facilities: {row['Facilities']}")
        print("-" * 50)