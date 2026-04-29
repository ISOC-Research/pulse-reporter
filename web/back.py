import os, pathlib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from neo4j import GraphDatabase
from request_for_YPI.pulse_service import get_country_list, find_similar_countries

app = Flask(__name__, static_folder='.')
CORS(app)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
NEO4J_URI, NEO4J_AUTH = 'neo4j://iyp-bolt.ihr.live:7687', None 

def get_ipv6_infrastructure(country_code):
    """STRICTLY for IPv6. Bypasses Neo4j for everything else."""
    path = PROJECT_ROOT / "request_for_YPI/security/enabling_technologies/ipv6_adoption/1.cypher"
    if not path.exists(): return None
    
    try:
        query = path.read_text(encoding='utf-8')
        with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
            records, _, _ = driver.execute_query(query, {"countryCode": country_code.upper()}, database_="neo4j")
            if records:
                val = records[0].get("percentage", 0.0)
                return val / 100.0 if val > 1.0 else val
    except Exception as e:
        print(f"Neo4j Error ({country_code}): {e}")
    return None

@app.route('/')
def index(): return send_from_directory(str(pathlib.Path(__file__).parent), 'result.html')

@app.route('/countries')
def countries(): return jsonify({"countries": get_country_list(2024)})

@app.route('/similar')
def similar():
    c, i = request.args.get("country"), request.args.get("indicator")
    try:
        data = find_similar_countries(c.upper(), 2024, i)
        if not data or "error" in data: return jsonify({"error": "No data found"}), 404

        # 🚀 NARROW DOWN THE LIST: Cap the table to 10 items max
        if data.get("similar"):
            peer_list = data["similar"][:10]
        else:
            # For Binary (DNSSEC/HTTPS), grab a sample of 5 'same' and 5 'different'
            peer_list = data.get("same_group", [])[:5] + data.get("different_group", [])[:5]

        # 🚀 ONLY USE NEO4J IF INDICATOR IS IPV6
        if i == "ipv6":
            data["reference"]["neo4j_average"] = get_ipv6_infrastructure(c)
            for p in peer_list: p["neo4j_average"] = get_ipv6_infrastructure(p.get("country"))
        
        data["peers_fused"] = peer_list
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=True)