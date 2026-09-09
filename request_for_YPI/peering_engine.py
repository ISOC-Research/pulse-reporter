import pathlib
import pprint
import sys
from collections import Counter
from contextlib import redirect_stdout

import requests

# ============================================================
# PROJECT PATH
# ============================================================

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# ============================================================
# API CONFIGURATION
# ============================================================

RIPESTAT_BASE_URL = "https://stat.ripe.net/data"
PEERINGDB_BASE_URL = "https://www.peeringdb.com/api"
PCH_IXP_URL = "https://www.pch.net/api/ixp/directory/Active"


# ============================================================
# GENERIC RIPEstat REQUEST
# ============================================================

def _query_ripestat(endpoint: str, params: dict) -> dict:
    """
    Generic RIPEstat Data API request.
    """

    url = f"{RIPESTAT_BASE_URL}/{endpoint}/data.json"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if result.get("status") != "ok":
            raise RuntimeError(
                result.get(
                    "status_message",
                    "RIPEstat request failed"
                )
            )

        return result

    except requests.RequestException as e:
        raise RuntimeError(
            f"RIPEstat request failed: {str(e)}"
        )


# ============================================================
# GENERIC PeeringDB REQUEST
# ============================================================

def _query_peeringdb(
    endpoint: str,
    params: dict | None = None
) -> list:
    """
    Generic PeeringDB API request.

    Returns:
        List of records from the PeeringDB 'data' field.
    """

    url = f"{PEERINGDB_BASE_URL}/{endpoint}"

    try:
        response = requests.get(
            url,
            params=params or {},
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result.get("data", [])

    except requests.RequestException as e:
        raise RuntimeError(
            f"PeeringDB request failed: {str(e)}"
        )


# ============================================================
# 1.1 — REGISTERED VS ROUTED ASNs
# ============================================================

def get_asn_landscape(country_code: str) -> dict:
    """
    Compare registered ASNs with routed ASNs for a country.

    Registered:
        ASNs associated with the country according to RIR data.

    Routed:
        ASNs visible/routed according to RIPEstat.

    This is the project's definition for the macro-level
    ASN landscape metric.
    """

    country_code = country_code.upper()

    try:

        response = requests.get(
            "https://stat.ripe.net/data/country-asns/data.json",
            params={
                "resource": country_code
            },
            timeout=30
        )

        response.raise_for_status()

        payload = response.json()

        data = payload.get(
            "data",
            {}
        )

        countries = data.get(
            "countries",
            []
        )

        if not countries:

            return {
                "metric": "asn_landscape",
                "country": country_code,
                "registered_asns": None,
                "routed_asns": None,
                "non_routed_asns": None,
                "routed_percentage": None,
                "source": "RIPEstat",
                "method": "RIPEstat country-asns",
                "status": "error",
                "error": (
                    "RIPEstat country-asns response "
                    "contains no country data."
                )
            }

        stats = countries[0].get(
            "stats",
            {}
        )

        registered = stats.get(
            "registered"
        )

        routed = stats.get(
            "routed"
        )

        if registered is None or routed is None:

            return {
                "metric": "asn_landscape",
                "country": country_code,
                "registered_asns": None,
                "routed_asns": None,
                "non_routed_asns": None,
                "routed_percentage": None,
                "source": "RIPEstat",
                "method": "RIPEstat country-asns",
                "status": "error",
                "error": (
                    "RIPEstat country-asns response "
                    "does not contain registered/routed values."
                )
            }

        non_routed = registered - routed

        routed_percentage = (
            round(
                (routed / registered) * 100,
                2
            )
            if registered > 0
            else None
        )

        return {
            "metric": "asn_landscape",
            "country": country_code,
            "registered_asns": registered,
            "routed_asns": routed,
            "non_routed_asns": non_routed,
            "routed_percentage": routed_percentage,
            "unit": "ASNs",
            "source": "RIPEstat",
            "method": (
                "RIPEstat country-asns: "
                "registered vs routed ASNs"
            ),
            "status": "measured",
            "error": None
        }

    except Exception as e:

        return {
            "metric": "asn_landscape",
            "country": country_code,
            "registered_asns": None,
            "routed_asns": None,
            "non_routed_asns": None,
            "routed_percentage": None,
            "source": "RIPEstat",
            "method": "RIPEstat country-asns",
            "status": "error",
            "error": str(e)
        }


# ============================================================
# COUNTRY ASN INVENTORY
# ============================================================

def get_country_asns(country_code: str) -> dict:
    """
    Get the complete country-associated ASN inventory
    from RIPEstat.
    """

    country_code = country_code.upper()

    try:

        result = _query_ripestat(
            "country-resource-list",
            {
                "resource": country_code
            }
        )

        data = result.get(
            "data",
            {}
        )

        resources = data.get(
            "resources",
            {}
        )

        asns = resources.get(
            "asn",
            []
        )

        return {
            "metric": "country_asn_inventory",
            "country": country_code,
            "asn_count": len(asns),
            "asns": asns,
            "source": "RIPEstat",
            "method": (
                "Country resource list ASN inventory"
            ),
            "status": "measured",
            "error": None
        }

    except Exception as e:

        return {
            "metric": "country_asn_inventory",
            "country": country_code,
            "asn_count": None,
            "asns": [],
            "source": "RIPEstat",
            "method": (
                "Country resource list ASN inventory"
            ),
            "status": "error",
            "error": str(e)
        }


# ============================================================
# ASN NEIGHBOURS
# ============================================================

def get_asn_neighbours(asn: int | str) -> dict:
    """
    Get BGP neighbours for a representative ASN.
    """

    asn = str(asn)

    try:

        result = _query_ripestat(
            "asn-neighbours",
            {
                "resource": asn
            }
        )

        data = result.get(
            "data",
            {}
        )

        counts = data.get(
            "neighbour_counts",
            {}
        )

        neighbours = data.get(
            "neighbours",
            []
        )

        return {
            "metric": "asn_neighbours",
            "asn": int(asn),
            "unique_neighbours": counts.get(
                "unique"
            ),
            "left_neighbours": counts.get(
                "left"
            ),
            "right_neighbours": counts.get(
                "right"
            ),
            "uncertain_neighbours": counts.get(
                "uncertain"
            ),
            "neighbours": neighbours,
            "source": "RIPEstat",
            "method": (
                "RIPEstat BGP ASN neighbour analysis"
            ),
            "status": "measured",
            "error": None
        }

    except Exception as e:

        return {
            "metric": "asn_neighbours",
            "asn": int(asn),
            "unique_neighbours": None,
            "left_neighbours": None,
            "right_neighbours": None,
            "uncertain_neighbours": None,
            "neighbours": [],
            "source": "RIPEstat",
            "method": (
                "RIPEstat BGP ASN neighbour analysis"
            ),
            "status": "error",
            "error": str(e)
        }


# ============================================================
# AS PATH LENGTH
# ============================================================

def get_as_path_length(asn: int | str) -> dict:
    """
    Get AS-path length statistics for a representative ASN.
    """

    asn = str(asn)

    try:

        result = _query_ripestat(
            "as-path-length",
            {
                "resource": asn
            }
        )

        data = result.get(
            "data",
            {}
        )

        stats = data.get(
            "stats",
            []
        )

        return {
            "metric": "as_path_length",
            "asn": int(asn),
            "stats": stats,
            "source": "RIPEstat",
            "method": (
                "RIPEstat AS-path length analysis"
            ),
            "status": "measured",
            "error": None
        }

    except Exception as e:

        return {
            "metric": "as_path_length",
            "asn": int(asn),
            "stats": [],
            "source": "RIPEstat",
            "method": (
                "RIPEstat AS-path length analysis"
            ),
            "status": "error",
            "error": str(e)
        }


# ============================================================
# 2.1 — IXP ACTIVITY / OPERATIONAL STATUS
# ============================================================

def get_ixp_activity(country_code: str) -> dict:
    """
    Analyze domestic IXPs using PeeringDB.

    Important:
        PeeringDB 'status=ok' indicates an operational/valid
        PeeringDB record. It does NOT by itself prove that
        traffic is currently flowing.

        Therefore:

            operational_ixps = status == 'ok'

        and:

            ixps_with_networks = net_count > 0

        is treated as a participation/activity proxy.

    This avoids incorrectly claiming that PeeringDB directly
    measures real-time traffic activity.
    """

    country_code = country_code.upper()

    try:

        ixps = _query_peeringdb(
            "ix",
            {
                "country": country_code,
                "limit": 200
            }
        )

        total_ixps = len(ixps)

        operational_ixps = [
            ixp
            for ixp in ixps
            if ixp.get("status") == "ok"
        ]

        ixps_with_networks = [
            ixp
            for ixp in operational_ixps
            if (ixp.get("net_count") or 0) > 0
        ]

        ixps_without_networks = [
            ixp
            for ixp in operational_ixps
            if (ixp.get("net_count") or 0) == 0
        ]

        return {
            "metric": "ixp_activity",
            "country": country_code,

            "total_ixps": total_ixps,

            "operational_ixps": len(
                operational_ixps
            ),

            "ixps_with_networks": len(
                ixps_with_networks
            ),

            "ixps_without_networks": len(
                ixps_without_networks
            ),

            "participation_proxy_percentage": (
                round(
                    (
                        len(ixps_with_networks)
                        / total_ixps
                    ) * 100,
                    2
                )
                if total_ixps > 0
                else None
            ),

            "ixps": [
                {
                    "name": ixp.get("name"),
                    "city": ixp.get("city"),
                    "status": ixp.get("status"),
                    "net_count": ixp.get("net_count"),
                    "fac_count": ixp.get("fac_count"),
                    "ixf_net_count": ixp.get(
                        "ixf_net_count"
                    ),
                    "updated": ixp.get("updated")
                }
                for ixp in ixps
            ],

            "source": "PeeringDB",

            "method": (
                "PeeringDB IXP records. status=ok is used "
                "as an operational-record indicator and "
                "net_count>0 as a participation/activity proxy. "
                "This is not a direct real-time traffic measurement."
            ),

            "status": "measured",

            "error": None
        }

    except Exception as e:

        return {
            "metric": "ixp_activity",
            "country": country_code,
            "total_ixps": None,
            "operational_ixps": None,
            "ixps_with_networks": None,
            "ixps_without_networks": None,
            "participation_proxy_percentage": None,
            "ixps": [],
            "source": "PeeringDB",
            "method": "PeeringDB IXP API",
            "status": "error",
            "error": str(e)
        }


# ============================================================
# 2.2 — IXP GEOGRAPHIC DISTRIBUTION
# ============================================================

def _normalize_city(city: str | None) -> str:
    """
    Normalize common city-name variations so that
    Bangalore and Bengaluru are counted together.
    """

    if not city:
        return "Unknown"

    city = city.strip()

    city_lower = city.lower()

    if city_lower in {
        "bangalore",
        "bengaluru"
    }:
        return "Bengaluru"

    if city_lower in {
        "delhi",
        "new delhi"
    }:
        return "Delhi"

    return city


def get_ixp_geographic_distribution(
    country_code: str
) -> dict:
    """
    Analyze geographic distribution of domestic IXPs
    using the city field from PeeringDB.
    """

    country_code = country_code.upper()

    try:

        ixps = _query_peeringdb(
            "ix",
            {
                "country": country_code,
                "limit": 200
            }
        )

        if not ixps:

            return {
                "metric": "ixp_geographic_distribution",
                "country": country_code,
                "ixp_count": 0,
                "city_count": 0,
                "cities": [],
                "source": "PeeringDB",
                "method": (
                    "IXP city distribution from PeeringDB"
                ),
                "status": "measured",
                "error": None
            }

        city_counts = Counter(
            _normalize_city(
                ixp.get("city")
            )
            for ixp in ixps
        )

        cities = []

        for city, count in city_counts.most_common():

            percentage = (
                count / len(ixps)
            ) * 100

            cities.append({
                "city": city,
                "ixp_count": count,
                "percentage": round(
                    percentage,
                    2
                )
            })

        # ----------------------------------------------------
        # Concentration indicators
        # ----------------------------------------------------

        top_city = (
            cities[0]
            if cities
            else None
        )

        top_city_percentage = (
            top_city["percentage"]
            if top_city
            else None
        )

        # Herfindahl-style concentration index.
        #
        # HHI = sum(city_share^2)
        #
        # Share is expressed as a fraction between 0 and 1.

        geographic_hhi = round(
            sum(
                (
                    city["ixp_count"]
                    / len(ixps)
                ) ** 2
                for city in cities
            ),
            4
        )

        return {
            "metric": "ixp_geographic_distribution",
            "country": country_code,

            "ixp_count": len(ixps),

            "city_count": len(
                city_counts
            ),

            "cities": cities,

            "largest_city": (
                top_city["city"]
                if top_city
                else None
            ),

            "largest_city_ixp_count": (
                top_city["ixp_count"]
                if top_city
                else None
            ),

            "largest_city_percentage": (
                top_city_percentage
            ),

            "geographic_hhi": geographic_hhi,

            "source": "PeeringDB",

            "method": (
                "IXP geographic distribution by city from "
                "PeeringDB. Common city-name variants such "
                "as Bangalore/Bengaluru are normalized."
            ),

            "status": "measured",

            "error": None
        }

    except Exception as e:

        return {
            "metric": "ixp_geographic_distribution",
            "country": country_code,
            "ixp_count": None,
            "city_count": None,
            "cities": [],
            "largest_city": None,
            "largest_city_ixp_count": None,
            "largest_city_percentage": None,
            "geographic_hhi": None,
            "source": "PeeringDB",
            "method": (
                "IXP city distribution from PeeringDB"
            ),
            "status": "error",
            "error": str(e)
        }


# ============================================================
# 2.3 — AGGREGATED IXP TRAFFIC
# ============================================================

def get_ixp_traffic(country_code: str) -> dict:
    """
    Calculate aggregated domestic IXP traffic using PCH.

    PCH provides IXP-level traffic values through its active
    IXP directory.

    Fields used:

        traf:
            Reported peak IPv4 traffic.

        avg:
            Reported average IPv4 traffic.

    The values returned by PCH are treated as bits per second
    and converted to Gbps.

    Important:
        This metric only includes Indian IXPs present in the
        PCH active directory. It therefore does not necessarily
        represent every IXP listed by PeeringDB.

        It should be interpreted as:

            "Aggregated PCH-reported IPv4 IXP traffic"

        rather than total IPv4 + IPv6 traffic across every
        domestic exchange.
    """

    country_code = country_code.upper()

    # PCH uses country names rather than ISO-2 codes.
    country_names = {
        "IN": "India",
        "FR": "France",
        "US": "United States",
        "GB": "United Kingdom",
        "DE": "Germany",
        "SG": "Singapore",
        "AU": "Australia",
        "BR": "Brazil",
        "CA": "Canada",
        "JP": "Japan",
    }

    country_name = country_names.get(
        country_code
    )

    if not country_name:

        return {
            "metric": "aggregated_ixp_traffic",
            "country": country_code,
            "peak_traffic_gbps": None,
            "average_traffic_gbps": None,
            "ixp_count": 0,
            "ixps_with_peak_data": 0,
            "ixps_with_average_data": 0,
            "ixps_included": [],
            "source": "PCH",
            "method": (
                "Sum of PCH-reported peak and average "
                "IPv4 traffic across domestic IXPs"
            ),
            "status": "error",
            "error": (
                f"No PCH country-name mapping configured "
                f"for {country_code}"
            )
        }

    try:

        response = requests.get(
            PCH_IXP_URL,
            timeout=30
        )

        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, list):

            return {
                "metric": "aggregated_ixp_traffic",
                "country": country_code,
                "peak_traffic_gbps": None,
                "average_traffic_gbps": None,
                "ixp_count": 0,
                "ixps_with_peak_data": 0,
                "ixps_with_average_data": 0,
                "ixps_included": [],
                "source": "PCH",
                "method": (
                    "Sum of PCH-reported peak and average "
                    "IPv4 traffic across domestic IXPs"
                ),
                "status": "error",
                "error": (
                    "Unexpected PCH API response format"
                )
            }

        # --------------------------------------------------------
        # Filter IXPs belonging to the requested country
        # --------------------------------------------------------

        country_ixps = [
            ixp
            for ixp in payload
            if str(
                ixp.get("ctry", "")
            ).strip().lower()
            == country_name.lower()
        ]

        total_peak = 0.0
        total_average = 0.0

        peak_count = 0
        average_count = 0

        ixps_included = []

        # --------------------------------------------------------
        # Process individual IXPs
        # --------------------------------------------------------

        for ixp in country_ixps:

            name = ixp.get("name")
            city = ixp.get("cit")
            ixp_id = ixp.get("id")

            peak_raw = ixp.get("traf")
            average_raw = ixp.get("avg")

            # Safely parse peak traffic.
            #
            # PCH test results confirm these values are already
            # expressed as bits per second.
            try:
                peak = float(peak_raw)
            except (TypeError, ValueError):
                peak = 0.0

            # Safely parse average traffic.
            try:
                average = float(average_raw)
            except (TypeError, ValueError):
                average = 0.0

            # Aggregate only non-zero reported values.
            if peak > 0:
                total_peak += peak
                peak_count += 1

            if average > 0:
                total_average += average
                average_count += 1

            # Convert bits per second -> Gbps.
            peak_gbps = round(
                peak / 1_000_000_000,
                3
            )

            average_gbps = round(
                average / 1_000_000_000,
                3
            )

            ixps_included.append({
                "id": ixp_id,
                "name": name,
                "city": city,
                "status": ixp.get("stat"),
                "peak_traffic_gbps": peak_gbps,
                "average_traffic_gbps": average_gbps,
                "updated": ixp.get("updt")
            })

        # --------------------------------------------------------
        # Aggregate final values
        # --------------------------------------------------------

        total_peak_gbps = round(
            total_peak / 1_000_000_000,
            3
        )

        total_average_gbps = round(
            total_average / 1_000_000_000,
            3
        )

        # --------------------------------------------------------
        # Return structured metric
        # --------------------------------------------------------

        return {
            "metric": "aggregated_ixp_traffic",
            "country": country_code,

            "peak_traffic_gbps": total_peak_gbps,
            "average_traffic_gbps": total_average_gbps,

            "ixp_count": len(country_ixps),

            "ixps_with_peak_data": peak_count,

            "ixps_with_average_data": average_count,

            "ixps_included": ixps_included,

            "source": "PCH",

            "method": (
                "Sum of PCH-reported peak and average "
                "IPv4 traffic across domestic IXPs"
            ),

            "status": "measured",

            "error": None
        }

    except requests.RequestException as e:

        return {
            "metric": "aggregated_ixp_traffic",
            "country": country_code,
            "peak_traffic_gbps": None,
            "average_traffic_gbps": None,
            "ixp_count": 0,
            "ixps_with_peak_data": 0,
            "ixps_with_average_data": 0,
            "ixps_included": [],
            "source": "PCH",
            "method": (
                "Sum of PCH-reported peak and average "
                "IPv4 traffic across domestic IXPs"
            ),
            "status": "error",
            "error": str(e)
        }

    except Exception as e:

        return {
            "metric": "aggregated_ixp_traffic",
            "country": country_code,
            "peak_traffic_gbps": None,
            "average_traffic_gbps": None,
            "ixp_count": 0,
            "ixps_with_peak_data": 0,
            "ixps_with_average_data": 0,
            "ixps_included": [],
            "source": "PCH",
            "method": (
                "Sum of PCH-reported peak and average "
                "IPv4 traffic across domestic IXPs"
            ),
            "status": "error",
            "error": str(e)
        }


# ============================================================
# RIPEstat PEERING DATA
# ============================================================

def build_ripestat_peering_data(
    country_code: str,
    representative_asn: int | str | None = None
) -> dict:

    country_code = country_code.upper()

    result = {
        "country": country_code,

        "asn_landscape": None,

        "country_asn_inventory": None,

        "representative_asn": representative_asn,

        "asn_neighbours": None,

        "as_path_length": None,

        "sources": [
            "RIPEstat"
        ],

        "errors": []
    }

    # --------------------------------------------------------
    # ASN LANDSCAPE
    # --------------------------------------------------------

    landscape = get_asn_landscape(
        country_code
    )

    result["asn_landscape"] = landscape

    if landscape.get("error"):

        result["errors"].append({
            "metric": "asn_landscape",
            "error": landscape["error"]
        })

    # --------------------------------------------------------
    # COUNTRY ASN INVENTORY
    # --------------------------------------------------------

    inventory = get_country_asns(
        country_code
    )

    result["country_asn_inventory"] = inventory

    if inventory.get("error"):

        result["errors"].append({
            "metric": "country_asn_inventory",
            "error": inventory["error"]
        })

    # --------------------------------------------------------
    # REPRESENTATIVE ASN
    # --------------------------------------------------------

    if representative_asn is not None:

        neighbours = get_asn_neighbours(
            representative_asn
        )

        result["asn_neighbours"] = neighbours

        if neighbours.get("error"):

            result["errors"].append({
                "metric": "asn_neighbours",
                "error": neighbours["error"]
            })

        path_length = get_as_path_length(
            representative_asn
        )

        result["as_path_length"] = path_length

        if path_length.get("error"):

            result["errors"].append({
                "metric": "as_path_length",
                "error": path_length["error"]
            })

    return result


# ============================================================
# FULL PEERING REPORT DATA
# ============================================================

def build_peering_report_data(
    country_code: str,
    representative_asn: int | str | None = None
) -> dict:

    country_code = country_code.upper()

    # --------------------------------------------------------
    # RIPEstat
    # --------------------------------------------------------

    ripestat = build_ripestat_peering_data(
        country_code,
        representative_asn
    )

    # --------------------------------------------------------
    # PeeringDB — IXP Activity
    # --------------------------------------------------------

    ixp_activity = get_ixp_activity(
        country_code
    )

    # --------------------------------------------------------
    # PeeringDB — Geographic Distribution
    # --------------------------------------------------------

    ixp_geography = get_ixp_geographic_distribution(
        country_code
    )

    # --------------------------------------------------------
    # PCH — Aggregated IXP Traffic
    # --------------------------------------------------------

    ixp_traffic = get_ixp_traffic(
        country_code
    )

    # --------------------------------------------------------
    # Aggregate errors
    # --------------------------------------------------------

    errors = list(
        ripestat.get(
            "errors",
            []
        )
    )

    for metric_result in [
        ixp_activity,
        ixp_geography,
        ixp_traffic
    ]:

        if metric_result.get("status") == "error":

            errors.append({
                "metric": metric_result.get(
                    "metric"
                ),
                "error": metric_result.get(
                    "error"
                )
            })

    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    sources = [
        "RIPEstat",
        "PeeringDB"
    ]

    if ixp_traffic.get("source"):
        sources.append(
            ixp_traffic["source"]
        )

    # Remove duplicates while preserving order.
    sources = list(
        dict.fromkeys(sources)
    )

    # --------------------------------------------------------
    # FINAL STRUCTURE
    # --------------------------------------------------------

    return {

        "country": country_code,

        # ====================================================
        # 1. MACRO NETWORK LANDSCAPE
        # ====================================================

        "macro_network": {

            "asn_landscape":
                ripestat[
                    "asn_landscape"
                ],

            "country_asn_inventory":
                ripestat[
                    "country_asn_inventory"
                ]
        },

        # ====================================================
        # 2. IXP INFRASTRUCTURE & HEALTH
        # ====================================================

        "ixp_infrastructure": {

            # 2.1
            "ixp_activity":
                ixp_activity,

            # 2.2
            "geographic_distribution":
                ixp_geography,

            # 2.3
            "aggregated_ixp_traffic":
                ixp_traffic
        },

        # ====================================================
        # 3. PEERING PARTICIPATION & REACHABILITY
        # ====================================================

        "peering_participation": {

            "ixp_penetration": {

                "metric": "ixp_penetration_rate",

                "status": "not_implemented",

                "source": "IYP / PeeringDB",

                "method": (
                    "Active/routed country ASNs that are "
                    "members of at least one domestic IXP "
                    "divided by total active/routed ASNs."
                )
            },

            "route_server_utilization": {

                "metric": "route_server_utilization",

                "status": "not_implemented",

                "source": "PeeringDB"
            }
        },

        # ====================================================
        # 4. CONTENT LOCALIZATION & CDNs
        # ====================================================

        "content_localization": {

            "global_cdn_presence": {

                "metric": "global_cdn_presence",

                "status": "not_implemented",

                "source": "PeeringDB"
            },

            "onnet_caching_nodes": {

                "metric": "onnet_caching_nodes",

                "status": "not_implemented",

                "source": "PeeringDB / CDN sources"
            },

            "localization_ratio": {

                "metric": "localization_ratio",

                "status": "not_implemented",

                "source": "Cloudflare Radar"
            }
        },

        # ====================================================
        # 5. ROUTING / PERFORMANCE
        # ====================================================

        "routing_performance": {

            "domestic_tromboning": {

                "metric": "domestic_tromboning",

                "status": "not_implemented",

                "source": "RIPE Atlas"
            },

            "edge_content_latency": {

                "metric": "edge_content_latency",

                "status": "not_implemented",

                "source": "RIPE Atlas"
            },

            "ripestat_asn_analysis": {

                "representative_asn":
                    ripestat[
                        "representative_asn"
                    ],

                "asn_neighbours":
                    ripestat[
                        "asn_neighbours"
                    ],

                "as_path_length":
                    ripestat[
                        "as_path_length"
                    ]
            }
        },

        # ====================================================
        # SOURCES / ERRORS
        # ====================================================

        "sources": sources,

        "errors": errors
    }


# ============================================================
# LOCAL TEST + SAVE OUTPUT
# ============================================================

if __name__ == "__main__":

    COUNTRY = "IN"

    REPRESENTATIVE_ASN = 9829

    OUTPUT_FILE = (
        _ROOT
        / "testfiles"
        / "peering_engine_output.txt"
    )

    def run_test():

        print("=" * 70)
        print("PEERING ENGINE TEST")
        print("=" * 70)

        print(
            "Country:",
            COUNTRY
        )

        print(
            "Representative ASN:",
            REPRESENTATIVE_ASN
        )

        print(
            "Output:",
            OUTPUT_FILE
        )

        print()

        print(
            "Running Peering Engine..."
        )

        print()

        data = build_peering_report_data(
            COUNTRY,
            representative_asn=REPRESENTATIVE_ASN
        )

        print("=" * 70)
        print("PEERING ENGINE OUTPUT")
        print("=" * 70)

        pprint.pprint(
            data,
            sort_dicts=False,
            width=120
        )

        print()

        print("=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)

    # --------------------------------------------------------
    # SAVE OUTPUT
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f, redirect_stdout(f):

        run_test()

    print(
        "Peering engine test completed."
    )

    print(
        f"Output saved to: {OUTPUT_FILE}"
    )