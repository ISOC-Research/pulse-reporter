"""
Full audit test for peering_engine.py
Tests all implemented metrics in order with a sleep between PeeringDB calls.
"""
import sys
import time

sys.path.insert(0, r"C:\CollegeWork\SummerInternship2\ISOC_Workspace\pulse-reporter")

from request_for_YPI.peering_engine import (
    get_asn_landscape,
    get_ixp_activity,
    get_ixp_geographic_distribution,
    get_ixp_traffic,
    _fetch_ixp_netixlans,
    get_peering_participation,
    get_cdn_presence,
)

COUNTRY = "IN"
results = {}

print("=" * 60)
print("PEERING ENGINE FULL AUDIT — Country:", COUNTRY)
print("=" * 60)

print("\n--- 1.1 Registered vs. Routed ASNs (RIPEstat) ---")
r = get_asn_landscape(COUNTRY)
print(f"  status      : {r.get('status')}")
print(f"  registered  : {r.get('registered_asns')}")
print(f"  routed      : {r.get('routed_asns')}")
print(f"  routed %    : {r.get('routed_percentage')}%")
results["1.1 ASN Landscape"] = r.get("status")
total_active_asns = r.get("routed_asns", 0)

print("\n--- 2.1 Active vs. Inactive IXPs (PeeringDB) ---")
r = get_ixp_activity(COUNTRY)
print(f"  status              : {r.get('status')}")
print(f"  total IXPs          : {r.get('total_ixps')}")
print(f"  IXPs with networks  : {r.get('ixps_with_networks')}")
print(f"  participation proxy : {r.get('participation_proxy_percentage')}%")
results["2.1 IXP Activity"] = r.get("status")

print("\n--- 2.2 Geographic Distribution (PeeringDB) ---")
r = get_ixp_geographic_distribution(COUNTRY)
print(f"  status  : {r.get('status')}")
print(f"  cities  : {r.get('city_count')}")
print(f"  HHI     : {r.get('herfindahl_hirschman_index')}")
results["2.2 IXP Geography"] = r.get("status")

print("\n--- 2.3 Aggregated IXP Traffic (PCH) ---")
r = get_ixp_traffic(COUNTRY)
print(f"  status        : {r.get('status')}")
print(f"  peak Gbps     : {r.get('peak_traffic_gbps')}")
print(f"  average Gbps  : {r.get('average_traffic_gbps')}")
results["2.3 IXP Traffic"] = r.get("status")

print("\n--- Waiting 10s before PeeringDB netixlan fetch ---")
time.sleep(10)

print("\n--- Fetching shared PeeringDB IXP + netixlan records ---")
try:
    _, shared_netixlans = _fetch_ixp_netixlans(COUNTRY)
    print(f"  SUCCESS — {len(shared_netixlans)} netixlan records fetched")
    shared_ok = True
except Exception as e:
    print(f"  FAILED — {e}")
    shared_netixlans = None
    shared_ok = False

print("\n--- Fetching active ASN list for 3.1+3.2 (from RIPEstat) ---")
from request_for_YPI.peering_engine import get_country_asns
asn_data = get_country_asns(COUNTRY)
active_asns = asn_data.get("asns", [])
print(f"  active ASNs retrieved: {len(active_asns)}")

print("\n--- 3.1 + 3.2 Peering Participation (PeeringDB) ---")
r = get_peering_participation(COUNTRY, active_asns, total_active_asns, netixlans=shared_netixlans)
print(f"  status                 : {r.get('status')}")
print(f"  ixp_penetration_rate   : {r.get('ixp_penetration_rate')}%")
print(f"  route_server_util      : {r.get('route_server_utilization')}%")
print(f"  peering_asn_count      : {r.get('peering_asn_count')}")
print(f"  rs_peering_asn_count   : {r.get('rs_peering_asn_count')}")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["3.1+3.2 Peering Participation"] = r.get("status")

print("\n--- 4.1 Global CDN Presence (PeeringDB) ---")
r = get_cdn_presence(COUNTRY, netixlans=shared_netixlans)
print(f"  status     : {r.get('status')}")
print(f"  cdn_count  : {r.get('cdn_count')}")
for cdn in r.get("cdns_present", []):
    print(f"   - {cdn['name']} (AS{cdn['asn']})")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["4.1 CDN Presence"] = r.get("status")

print("\n--- Waiting 5s before 4.2 On-Net Caching fetch ---")
time.sleep(5)

from request_for_YPI.peering_engine import get_on_net_caching_nodes, get_localization_ratio

print("\n--- 4.2 On-Net Caching Nodes (PeeringDB netfac) ---")
r = get_on_net_caching_nodes(COUNTRY)
print(f"  status     : {r.get('status')}")
print(f"  cdn_count  : {r.get('cdn_count')}")
for cdn in r.get("cdns_in_local_facilities", []):
    print(f"   - {cdn['name']} (AS{cdn['asn']})")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["4.2 On-Net Caching"] = r.get("status")

print("\n--- 4.3 Localization Ratio (ISOC Pulse API) ---")
r = get_localization_ratio(COUNTRY)
print(f"  status                   : {r.get('status')}")
print(f"  peering_efficiency_score : {r.get('peering_efficiency_score')}")
print(f"  localization_percentage  : {r.get('localization_percentage')}%")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["4.3 Localization Ratio"] = r.get("status")

from request_for_YPI.peering_engine import get_domestic_tromboning, get_eyeball_latency

print("\n--- 5.1 Domestic Tromboning (RIPE Atlas) ---")
r = get_domestic_tromboning(COUNTRY)
print(f"  status               : {r.get('status')}")
print(f"  tromboning_pct       : {r.get('tromboning_percentage')}%")
print(f"  paths_analyzed       : {r.get('domestic_paths_analyzed')}")
print(f"  tromboned_count      : {r.get('tromboned_paths_count')}")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["5.1 Domestic Tromboning"] = r.get("status")

print("\n--- 5.2 Eyeball Latency to Edge Content (RIPE Atlas) ---")
r = get_eyeball_latency(COUNTRY)
print(f"  status               : {r.get('status')}")
print(f"  median_latency_ms    : {r.get('median_latency_ms')} ms")
print(f"  min_latency_ms       : {r.get('min_latency_ms')} ms")
print(f"  max_latency_ms       : {r.get('max_latency_ms')} ms")
print(f"  probes_sampled       : {r.get('probes_sampled')}")
if r.get("error"):
    print(f"  error: {r.get('error')}")
results["5.2 Eyeball Latency"] = r.get("status")


print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
for metric, status in results.items():
    if status == "measured":
        icon = "[OK ]"
    elif status == "error":
        icon = "[ERR]"
    else:
        icon = "[N/A]"
    print(f"  {icon}  {metric}: {status}")
print()
