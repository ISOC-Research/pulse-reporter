from request_for_YPI.pulse_service import (
    get_country_list,
    extract_all_countries_indicator,
    find_similar_countries
)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pathlib

app = Flask(__name__, static_folder='.')
CORS(app)

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]


# =========================
# 🌐 MAIN UI
# =========================
@app.route('/')
def index():
    return send_from_directory(str(pathlib.Path(__file__).parent), 'result.html')


# =========================
# 🌍 GET COUNTRIES
# =========================
@app.route('/countries', methods=['GET'])
def countries():
    year = request.args.get("year", default=2024, type=int)

    try:
        countries = get_country_list(year)
        return jsonify({"countries": countries})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 📊 GENERIC INDICATOR ENDPOINT
# =========================
@app.route('/indicator', methods=['GET'])
def indicator():
    year = request.args.get("year", default=2024, type=int)
    indicator = request.args.get("indicator", default="ipv6")

    try:
        data = extract_all_countries_indicator(year, indicator)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🔍 SIMILAR COUNTRIES
# =========================
@app.route('/similar', methods=['GET'])
def similar():
    country = request.args.get("country")
    indicator = request.args.get("indicator", default="ipv6")
    year = request.args.get("year", default=2024, type=int)

    if not country:
        return jsonify({"error": "Missing country"}), 400

    # Normalize
    country = country.upper()

    try:
        result = find_similar_countries(country, year, indicator)

        if not result:
            return jsonify({"error": "Country not found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)