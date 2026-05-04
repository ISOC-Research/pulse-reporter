import os, pathlib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from neo4j import GraphDatabase

# 🔥 Existing imports
from request_for_YPI.pulse_service import (
    get_country_list,
    find_similar_countries,
    get_asn_by_country   # ✅ NEW IMPORT
)

app = Flask(__name__, static_folder='.')
CORS(app)

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]

NEO4J_URI = 'neo4j://iyp-bolt.ihr.live:7687'
NEO4J_AUTH = None


# =========================
# 🌐 MAIN UI
# =========================
@app.route('/')
def index():
    return send_from_directory(str(pathlib.Path(__file__).parent), 'result.html')


# =========================
# 🌍 GET COUNTRIES
# =========================
@app.route('/countries')
def countries():
    return jsonify({"countries": get_country_list(2024)})


# =========================
# 🔍 SIMILAR COUNTRIES
# =========================
def get_ipv6_infrastructure(country_code):
    """STRICTLY for IPv6 (Neo4j-based infra metric)"""
    path = PROJECT_ROOT / "request_for_YPI/security/enabling_technologies/ipv6_adoption/1.cypher"
    if not path.exists():
        return None

    try:
        query = path.read_text(encoding='utf-8')

        with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
            records, _, _ = driver.execute_query(
                query,
                {"countryCode": country_code.upper()},
                database_="neo4j"
            )

            if records:
                val = records[0].get("ipv6PrefixesPercentage", 0.0)
                return val / 100.0 if val > 1.0 else val

    except Exception as e:
        print(f"Neo4j Error ({country_code}): {e}")

    return None


@app.route('/similar')
def similar():
    c = request.args.get("country")
    i = request.args.get("indicator")

    try:
        data = find_similar_countries(c.upper(), 2024, i)

        if not data or "error" in data:
            return jsonify({"error": "No data found"}), 404

        # 🔥 LIMIT RESULTS
        if data.get("similar"):
            peer_list = data["similar"][:10]
        else:
            peer_list = data.get("same_group", [])[:5] + data.get("different_group", [])[:5]

        # 🔥 ONLY USE NEO4J FOR IPV6
        if i == "ipv6":
            data["reference"]["neo4j_average"] = get_ipv6_infrastructure(c)

            for p in peer_list:
                p["neo4j_average"] = get_ipv6_infrastructure(p.get("country"))

        data["peers_fused"] = peer_list

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🧠 ASN / ISP DATA (NEW)
# =========================
@app.route('/asn', methods=['GET'])
def asn():
    country = request.args.get("country")

    if not country:
        return jsonify({"error": "Missing country"}), 400

    try:
        data = get_asn_by_country(country.upper())

        if isinstance(data, dict) and "error" in data:
            return jsonify(data), 500

        return jsonify({
            "country": country.upper(),
            "asns": data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)