import os
import json
import socket
from typing import Dict, Any, List
from urllib.parse import urlparse

# ── Langfuse: only enable tracing when properly configured ────────────────────
if os.environ.get("LANGFUSE_PUBLIC_KEY"):
    from langfuse import observe
else:
    # No-op decorator — avoids repeated "Authentication error" warnings
    def observe(**kwargs):
        def _passthrough(fn):
            return fn
        return _passthrough

from neo4j import GraphDatabase, basic_auth

def serialize_neo4j_values(value):
    if hasattr(value, 'iso_format'): return value.iso_format()
    if hasattr(value, 'to_native'): return value.to_native()
    if isinstance(value, list): return [serialize_neo4j_values(v) for v in value]
    if isinstance(value, dict): return {k: serialize_neo4j_values(v) for k, v in value.items()}
    return value


def _resolve_uri_ipv4(uri: str) -> str:
    """
    Resolve the hostname in a Neo4j bolt URI to an IPv4 address
    and switch from neo4j:// to bolt:// protocol.

    neo4j:// performs routing discovery which re-resolves the hostname
    internally (re-triggering IPv6/NAT64 failures). bolt:// connects
    directly to the resolved IP, avoiding this entirely.

    Falls back to the original URI if resolution fails.
    """
    try:
        parsed = urlparse(uri)
        hostname = parsed.hostname
        port = parsed.port or 7687
        # Force AF_INET (IPv4) resolution
        ipv4_addr = socket.getaddrinfo(hostname, port, socket.AF_INET)[0][4][0]
        resolved = uri.replace(hostname, ipv4_addr)
        # Switch neo4j:// → bolt:// to skip routing discovery
        resolved = resolved.replace("neo4j://", "bolt://")
        resolved = resolved.replace("neo4j+s://", "bolt+s://")
        return resolved
    except Exception:
        return uri  # fall back to original


import atexit

# Global connection pool for Neo4j
_neo4j_driver = None

def _get_driver():
    """Returns a globally cached Neo4j driver, creating it if necessary."""
    global _neo4j_driver
    if _neo4j_driver is None:
        URI = os.getenv("NEO4J_URI", "neo4j://iyp-bolt.ihr.live:7687")
        USER = os.getenv("NEO4J_USERNAME", "neo4j")
        PASSWORD = os.getenv("NEO4J_PASSWORD", "") 
        # Force IPv4 + direct bolt connection to avoid NAT64/IPv6 routing issues
        URI = _resolve_uri_ipv4(URI)
        _neo4j_driver = GraphDatabase.driver(URI, auth=basic_auth(USER, PASSWORD) if PASSWORD else None)
    return _neo4j_driver

@atexit.register
def _close_driver():
    """Ensures the driver connection pool is cleanly shut down on exit."""
    global _neo4j_driver
    if _neo4j_driver is not None:
        _neo4j_driver.close()
        _neo4j_driver = None


@observe(name="Test_Neo4j_Query")
def execute_cypher_test(cypher_query: str, timeout_seconds=20) -> Dict[str, Any]:
    """Exécute une seule requête Cypher et renvoie un rapport de succès/échec."""
    
    query_result = {
        "cypher": cypher_query,
        "success": False,
        "data": [],
        "error": None,
        "count": 0
    }

    try:
        driver = _get_driver()
        with driver.session() as session:
            result = session.run(cypher_query, transaction_config={'timeout': timeout_seconds * 1000})
            records = [record.data() for record in result]
            
            query_result["success"] = True
            query_result["data"] = serialize_neo4j_values(records)
            query_result["count"] = len(records)
            
        # Notice: We no longer call driver.close() here!
        # The connection pool is kept alive for subsequent queries.
            
    except Exception as e:
        query_result["success"] = False
        query_result["error"] = str(e)
    
    return query_result