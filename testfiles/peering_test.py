import pathlib
import sys

# Add project root to Python path
_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from request_for_YPI.src.request_IYP.request_testing import execute_cypher_test

COUNTRY_CODE = "FR"


# ============================================================
# 1.1 — TOTAL REGISTERED ASNs VS ACTIVE ASNs
# ============================================================

query = f"""
MATCH (a:AS)-[:COUNTRY]->(c:Country {{country_code: '{COUNTRY_CODE}'}})
OPTIONAL MATCH (a)-[:ORIGINATE]->(pfx:Prefix)

WITH c, a, COUNT(pfx) AS pfxCount

WITH c,
     COUNT(DISTINCT a) AS TotalASes,
     COUNT(DISTINCT CASE WHEN pfxCount > 0 THEN a END) AS ActiveASes,
     COUNT(DISTINCT CASE WHEN pfxCount = 0 THEN a END) AS DormantASes

RETURN c.name AS Country,
       TotalASes,
       ActiveASes,
       DormantASes,
       ROUND(ActiveASes * 100.0 / TotalASes * 100) / 100 AS ActivePercent
"""

result = execute_cypher_test(query)

print("=" * 60)
print("PEERING TEST — 1.1 ASN LANDSCAPE")
print("=" * 60)

if not result["success"]:
    print("❌ Query failed")
    print(result["error"])
else:
    print("✅ Query succeeded")
    print()

    for row in result["data"]:
        print(f"Country:        {row.get('Country')}")
        print(f"Total ASNs:     {row.get('TotalASes')}")
        print(f"Active ASNs:    {row.get('ActiveASes')}")
        print(f"Dormant ASNs:   {row.get('DormantASes')}")
        print(f"Active %:       {row.get('ActivePercent')}%")

print()
print("Raw result:")
print(result)