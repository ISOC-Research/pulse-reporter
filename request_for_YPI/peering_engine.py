import os
import pathlib
import pprint
import sys
from collections import Counter
from contextlib import redirect_stdout

import requests
from dotenv import load_dotenv

# ============================================================
# PROJECT PATH
# ============================================================

_ROOT = pathlib.Path(__file__).resolve().parents[1]

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

load_dotenv(_ROOT / ".env")

# ============================================================
# API CONFIGURATION
# ============================================================

RIPESTAT_BASE_URL = "https://stat.ripe.net/data"
PEERINGDB_BASE_URL = "https://www.peeringdb.com/api"
PCH_IXP_URL = "https://www.pch.net/api/ixp/directory/Active"

# PeeringDB API key — authenticated requests get higher rate limits.
# Set PEERINGDB_API_KEY in your .env file.
_PEERINGDB_API_KEY = os.getenv("PEERINGDB_API_KEY", "").strip() or None

RIPE_ATLAS_BASE_URL = "https://atlas.ripe.net/api/v2"
_RIPE_ATLAS_API_KEY = os.getenv("RIPE_ATLAS_API_KEY", "").strip() or None


def _query_ripe_atlas(endpoint: str, params: dict | None = None) -> dict | list:
    """
    Generic RIPE Atlas API v2 request.
    """
    url = f"{RIPE_ATLAS_BASE_URL}/{endpoint}"
    headers = {}
    if _RIPE_ATLAS_API_KEY:
        headers["Authorization"] = f"Key {_RIPE_ATLAS_API_KEY}"

    try:
        response = requests.get(url, params=params or {}, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"RIPE Atlas request failed: {str(e)}")


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
    params: dict | None = None,
    max_retries: int = 4,
    base_backoff: float = 5.0
) -> list:
    """
    Generic PeeringDB API request with exponential backoff on 429 rate limits.

    Retries up to max_retries times, doubling the wait each time:
      Attempt 1: wait 5s
      Attempt 2: wait 10s
      Attempt 3: wait 20s
      Attempt 4: wait 40s

    Returns:
        List of records from the PeeringDB 'data' field.
    """
    import time

    url = f"{PEERINGDB_BASE_URL}/{endpoint}"

    headers = {}
    if _PEERINGDB_API_KEY:
        headers["Authorization"] = f"Api-Key {_PEERINGDB_API_KEY}"

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(
                url,
                params=params or {},
                headers=headers,
                timeout=30
            )

            if response.status_code == 429:
                if attempt < max_retries:
                    wait = base_backoff * (2 ** attempt)
                    time.sleep(wait)
                    continue
                else:
                    response.raise_for_status()

            response.raise_for_status()
            result = response.json()
            return result.get("data", [])

        except requests.RequestException as e:
            if attempt < max_retries and "429" in str(e):
                wait = base_backoff * (2 ** attempt)
                time.sleep(wait)
                continue
            raise RuntimeError(
                f"PeeringDB request failed: {str(e)}"
            )

    raise RuntimeError(
        f"PeeringDB request failed after {max_retries} retries: rate limited"
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
# SHARED: Fetch domestic IXP netixlan records (one API call)
# ============================================================

def _fetch_ixp_netixlans(country_code: str) -> tuple[list, list]:
    """
    Fetch all domestic IXP IDs and their netixlan membership records
    from PeeringDB using paginated requests.

    Uses limit=250 per page instead of limit=0 (unbounded) to avoid
    triggering PeeringDB's heavy-query rate limiter on the netixlan endpoint.

    Returns (ix_ids, netixlans) — both are lists.
    Raises on any PeeringDB failure so callers can catch and gracefully error.
    """
    ixps = _query_peeringdb("ix", {"country": country_code, "limit": 200})
    ix_ids = [ixp.get("id") for ixp in ixps if ixp.get("id")]

    if not ix_ids:
        raise ValueError(f"No IXPs found in PeeringDB for {country_code}")

    netixlans = []
    page_size = 250
    ix_chunk_size = 20

    for i in range(0, len(ix_ids), ix_chunk_size):
        chunk = ix_ids[i:i + ix_chunk_size]
        ix_ids_str = ",".join(map(str, chunk))

        # Paginate through results for this chunk of IXP IDs
        skip = 0
        while True:
            page = _query_peeringdb(
                "netixlan",
                {
                    "ix_id__in": ix_ids_str,
                    "limit": page_size,
                    "skip": skip
                }
            )
            netixlans.extend(page)
            if len(page) < page_size:
                # Fewer results than page size → we've reached the last page
                break
            skip += page_size

    return ix_ids, netixlans



# ============================================================
# 3. PEERING PARTICIPATION & REACHABILITY
# ============================================================

def get_peering_participation(
    country_code: str,
    active_asns: list,
    total_active_asns: int,
    netixlans: list | None = None
) -> dict:
    country_code = country_code.upper()
    try:
        if not total_active_asns or not active_asns:
            raise ValueError("No active ASNs provided.")

        # Use pre-fetched data if supplied, otherwise fetch now
        if netixlans is None:
            _, netixlans = _fetch_ixp_netixlans(country_code)

        active_asns_set = set(int(a) for a in active_asns)
        unique_peering_asns = set()
        rs_peering_asns = set()

        for record in netixlans:
            asn = record.get("asn")
            if asn in active_asns_set:
                unique_peering_asns.add(asn)
                if record.get("is_rs_peer"):
                    rs_peering_asns.add(asn)

        penetration_rate = round(
            (len(unique_peering_asns) / total_active_asns) * 100, 2
        )

        rs_utilization = 0.0
        if unique_peering_asns:
            rs_utilization = round(
                (len(rs_peering_asns) / len(unique_peering_asns)) * 100, 2
            )

        return {
            "metric": "peering_participation",
            "country": country_code,
            "ixp_penetration_rate": penetration_rate,
            "peering_asn_count": len(unique_peering_asns),
            "total_active_asns": total_active_asns,
            "route_server_utilization": rs_utilization,
            "rs_peering_asn_count": len(rs_peering_asns),
            "source": "PeeringDB",
            "method": "Intersection of routed ASNs and domestic IXP members",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "peering_participation",
            "country": country_code,
            "ixp_penetration_rate": None,
            "peering_asn_count": None,
            "total_active_asns": total_active_asns,
            "route_server_utilization": None,
            "rs_peering_asn_count": None,
            "source": "PeeringDB",
            "method": "Intersection of routed ASNs and domestic IXP members",
            "status": "error",
            "error": str(e)
        }


# ============================================================
# 4. CONTENT LOCALIZATION & CDNs
# ============================================================

TIER_1_CDNS = {
    15169: "Google",
    32934: "Meta",
    2906:  "Netflix",
    13335: "Cloudflare",
    20940: "Akamai",
    16509: "Amazon",
    8075:  "Microsoft",
    22822: "Limelight / Edgio",
    54113: "Fastly"
}


def get_cdn_presence(
    country_code: str,
    netixlans: list | None = None
) -> dict:
    country_code = country_code.upper()
    try:
        # Use pre-fetched data if supplied, otherwise fetch now
        if netixlans is None:
            _, netixlans = _fetch_ixp_netixlans(country_code)

        present_cdns = {}
        for record in netixlans:
            asn = record.get("asn")
            if asn in TIER_1_CDNS:
                present_cdns[TIER_1_CDNS[asn]] = asn

        cdn_list = [{"name": name, "asn": asn} for name, asn in present_cdns.items()]
        cdn_list.sort(key=lambda x: x["name"])

        return {
            "metric": "global_cdn_presence",
            "country": country_code,
            "cdns_present": cdn_list,
            "cdn_count": len(cdn_list),
            "source": "PeeringDB",
            "method": "Tier-1 CDN ASNs found at domestic IXPs",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "global_cdn_presence",
            "country": country_code,
            "cdns_present": [],
            "cdn_count": 0,
            "source": "PeeringDB",
            "method": "Tier-1 CDN ASNs found at domestic IXPs",
            "status": "error",
            "error": str(e)
        }


def get_on_net_caching_nodes(country_code: str) -> dict:
    """
    Proxy for detecting deep on-net/embedded caches (like Google GGC, Netflix OCA).
    Checks PeeringDB for local facilities (datacenters) in the country where
    Tier-1 CDN ASNs are physically present, which strongly implies private
    interconnection or edge nodes deep inside local ISP infrastructure.
    """
    country_code = country_code.upper()
    try:
        # Get all facilities in the target country
        facs = []
        skip_fac = 0
        while True:
            page = _query_peeringdb("fac", {"country": country_code, "limit": 250, "skip": skip_fac})
            facs.extend(page)
            if len(page) < 250:
                break
            skip_fac += 250
            
        fac_ids = [str(f.get("id")) for f in facs if f.get("id")]

        if not fac_ids:
            raise ValueError(f"No facilities found for {country_code}")

        # Fetch netfac (networks in facilities) for these facilities
        # Paginated to avoid 429
        netfacs = []
        page_size = 250
        fac_chunk_size = 50

        for i in range(0, len(fac_ids), fac_chunk_size):
            chunk = fac_ids[i:i + fac_chunk_size]
            fac_ids_str = ",".join(chunk)

            skip = 0
            while True:
                page = _query_peeringdb(
                    "netfac",
                    {"fac_id__in": fac_ids_str, "limit": page_size, "skip": skip}
                )
                netfacs.extend(page)
                if len(page) < page_size:
                    break
                skip += page_size

        # Find which major CDNs are present in these local facilities
        present_cdns = {}
        for nf in netfacs:
            asn = nf.get("local_asn")
            if asn in TIER_1_CDNS:
                present_cdns[TIER_1_CDNS[asn]] = asn

        cdn_list = [{"name": name, "asn": asn} for name, asn in present_cdns.items()]
        cdn_list.sort(key=lambda x: x["name"])

        return {
            "metric": "on_net_caching_nodes",
            "country": country_code,
            "cdns_in_local_facilities": cdn_list,
            "cdn_count": len(cdn_list),
            "source": "PeeringDB",
            "method": "Tier-1 CDN ASNs found inside local physical facilities (proxy for PNI/Embedded Caches)",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "on_net_caching_nodes",
            "country": country_code,
            "cdns_in_local_facilities": [],
            "cdn_count": 0,
            "source": "PeeringDB",
            "method": "Tier-1 CDN ASNs found inside local physical facilities (proxy for PNI/Embedded Caches)",
            "status": "error",
            "error": str(e)
        }


def get_localization_ratio(country_code: str) -> dict:
    """
    Fetches the 'peering_efficiency' metric from the ISOC Pulse API.
    This serves as the proxy for Localization Ratio, estimating the degree to which
    traffic is kept domestic rather than exiting to international transit.
    """
    import os
    country_code = country_code.upper()
    try:
        api_key = os.getenv("INTERNET_SOCIETY_API_KEY")
        if not api_key:
            raise ValueError("INTERNET_SOCIETY_API_KEY not found in environment")

        headers = {"Authorization": f"Bearer {api_key}"}
        url = "https://pulse-api.internetsociety.org/resilience?year=2024"

        # Note: We use the requests module directly here to hit the Pulse API,
        # which is different from our _query_peeringdb/_query_ripestat helpers.
        import requests
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json().get("data", [])

        # Find the country record
        country_data = next((d for d in data if d.get("country") == country_code), None)
        if not country_data:
            raise ValueError(f"No Pulse API data found for {country_code}")

        # Drill down to market_readiness -> traffic_localization -> peering_efficiency
        val = None
        try:
            indicators = country_data["pillars"]["market_readiness"]["dimensions"]["traffic_localization"]["indicators"]
            if "peering_efficiency" in indicators:
                val = indicators["peering_efficiency"]["value"]
        except KeyError:
            pass

        if val is None:
            raise ValueError("peering_efficiency indicator missing in Pulse data")

        return {
            "metric": "localization_ratio",
            "country": country_code,
            "peering_efficiency_score": val,
            "localization_percentage": round(val * 100, 2),
            "source": "ISOC Pulse API",
            "method": "ISOC Pulse Peering Efficiency indicator",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "localization_ratio",
            "country": country_code,
            "peering_efficiency_score": None,
            "localization_percentage": None,
            "source": "ISOC Pulse API",
            "method": "ISOC Pulse Peering Efficiency indicator",
            "status": "error",
            "error": str(e)
        }


# ============================================================
# 5. ROUTING & PERFORMANCE (RIPE Atlas)
# ============================================================

def get_domestic_tromboning(country_code: str) -> dict:
    """
    Measures domestic tromboning (boomerang routing) by analyzing traceroute paths
    between active RIPE Atlas anchors within the country.
    Detects if any intermediate hop leaves the national borders.
    """
    import time
    country_code = country_code.upper()
    try:
        # 1. Query active anchors in the country
        anchors_res = _query_ripe_atlas("anchors", {"country": country_code})
        anchors = [a for a in anchors_res.get("results", []) if not a.get("is_disabled")]

        if len(anchors) < 2:
            return {
                "metric": "domestic_tromboning",
                "country": country_code,
                "tromboning_percentage": None,
                "domestic_paths_analyzed": 0,
                "tromboned_paths_count": 0,
                "source": "RIPE Atlas",
                "method": "Anchoring Mesh Traceroute Path Analysis",
                "status": "not_applicable",
                "error": f"Fewer than 2 active anchors found in {country_code}"
            }

        # 2. Pick target anchor (e.g. Bangalore or Mumbai) and find its mesh traceroute measurement
        target_anchor = anchors[0]
        fqdn = target_anchor.get("fqdn")

        m_search = _query_ripe_atlas(
            "measurements",
            {"type": "traceroute", "target": fqdn, "status": 2}
        )
        m_results = m_search.get("results", [])

        if not m_results:
            raise ValueError(f"No active mesh traceroute found for anchor {fqdn}")

        mid = m_results[0]["id"]

        # 3. Source probes: other active anchor probes in the country
        src_probe_ids = [str(a["probe"]) for a in anchors[1:6] if a.get("probe")]
        if not src_probe_ids:
            # Fallback to general country probes
            probes_res = _query_ripe_atlas("probes", {"country_code": country_code, "status": 1, "page_size": 5})
            src_probe_ids = [str(p["id"]) for p in probes_res.get("results", [])[:5]]

        src_str = ",".join(src_probe_ids)
        start_time = int(time.time()) - 3600 * 6  # last 6 hours

        res_data = _query_ripe_atlas(f"measurements/{mid}/results", {"probe_ids": src_str, "start": start_time})
        if not isinstance(res_data, list):
            res_data = []

        total_paths = 0
        tromboned_count = 0
        ip_geo_cache = {}

        for p_trace in res_data[:15]:
            hops = p_trace.get("result", [])
            path_ips = []
            for h in hops:
                for r_entry in h.get("result", []):
                    ip = r_entry.get("from")
                    if ip and not ip.startswith(("10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.", "172.2", "172.3")):
                        path_ips.append(ip)
                        break

            if len(path_ips) >= 3:
                total_paths += 1
                is_tromboned = False

                for hop_ip in path_ips[1:-1]:
                    if hop_ip not in ip_geo_cache:
                        try:
                            geo_r = _query_ripestat("geoloc", {"resource": hop_ip})
                            locs = geo_r.get("located_resources", [])
                            if locs and locs[0].get("locations"):
                                ip_geo_cache[hop_ip] = locs[0]["locations"][0].get("country")
                            else:
                                ip_geo_cache[hop_ip] = country_code
                        except Exception:
                            ip_geo_cache[hop_ip] = country_code

                    hop_country = ip_geo_cache.get(hop_ip)
                    if hop_country and hop_country != country_code:
                        is_tromboned = True
                        break

                if is_tromboned:
                    tromboned_count += 1

        tromboning_pct = round((tromboned_count / total_paths * 100), 2) if total_paths > 0 else 0.0

        return {
            "metric": "domestic_tromboning",
            "country": country_code,
            "tromboning_percentage": tromboning_pct,
            "domestic_paths_analyzed": total_paths,
            "tromboned_paths_count": tromboned_count,
            "target_anchor": fqdn,
            "source": "RIPE Atlas",
            "method": "Anchoring Mesh Traceroute Path Geolocation Analysis",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "domestic_tromboning",
            "country": country_code,
            "tromboning_percentage": None,
            "domestic_paths_analyzed": 0,
            "tromboned_paths_count": 0,
            "target_anchor": None,
            "source": "RIPE Atlas",
            "method": "Anchoring Mesh Traceroute Path Geolocation Analysis",
            "status": "error",
            "error": str(e)
        }


def get_eyeball_latency(country_code: str) -> dict:
    """
    Measures median eyeball latency to edge content / anycast DNS infrastructure
    using live RIPE Atlas eyeball probe measurements.
    """
    import statistics
    import time
    country_code = country_code.upper()
    try:
        probes_res = _query_ripe_atlas("probes", {"country_code": country_code, "status": 1, "page_size": 20})
        probe_ids = [str(p["id"]) for p in probes_res.get("results", [])]

        if not probe_ids:
            raise ValueError(f"No active RIPE Atlas probes found in {country_code}")

        probe_sample = probe_ids[:15]
        probe_str = ",".join(probe_sample)
        start_time = int(time.time()) - 3600  # last 1 hour

        # Measurement 1004 (f.root-servers.net - heavily anycasted across domestic IXPs)
        res_data = _query_ripe_atlas(
            "measurements/1004/results",
            {"probe_ids": probe_str, "start": start_time}
        )
        if not isinstance(res_data, list):
            res_data = []

        rtts = [r["avg"] for r in res_data if isinstance(r, dict) and r.get("avg") is not None]

        if not rtts:
            # Fallback to measurement 1001 (k-root)
            res_data = _query_ripe_atlas(
                "measurements/1001/results",
                {"probe_ids": probe_str, "start": start_time}
            )
            rtts = [r["avg"] for r in res_data if isinstance(r, dict) and r.get("avg") is not None]

        if not rtts:
            raise ValueError("No recent latency measurements available from probes")

        median_lat = round(statistics.median(rtts), 2)
        min_lat = round(min(rtts), 2)
        max_lat = round(max(rtts), 2)

        return {
            "metric": "edge_content_latency",
            "country": country_code,
            "median_latency_ms": median_lat,
            "min_latency_ms": min_lat,
            "max_latency_ms": max_lat,
            "probes_sampled": len(probe_sample),
            "measurement_count": len(rtts),
            "target": "Edge Anycast DNS / Content Infrastructure",
            "source": "RIPE Atlas",
            "method": "Median RTT from in-country eyeball probes to edge anycast nodes",
            "status": "measured",
            "error": None
        }

    except Exception as e:
        return {
            "metric": "edge_content_latency",
            "country": country_code,
            "median_latency_ms": None,
            "min_latency_ms": None,
            "max_latency_ms": None,
            "probes_sampled": 0,
            "measurement_count": 0,
            "target": "Edge Anycast DNS / Content Infrastructure",
            "source": "RIPE Atlas",
            "method": "Median RTT from in-country eyeball probes to edge anycast nodes",
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

    print("  [1/9] Fetching RIPEstat inventory and routing data...")
    ripestat = build_ripestat_peering_data(
        country_code,
        representative_asn
    )

    # --------------------------------------------------------
    # PeeringDB — IXP Activity
    # --------------------------------------------------------

    print("  [2/9] Fetching IXP activity from PCH...")
    ixp_activity = get_ixp_activity(
        country_code
    )

    # --------------------------------------------------------
    # PeeringDB — Geographic Distribution
    # --------------------------------------------------------

    print("  [3/9] Analyzing IXP geographic distribution...")
    ixp_geography = get_ixp_geographic_distribution(
        country_code
    )

    # --------------------------------------------------------
    # PCH — Aggregated IXP Traffic
    # --------------------------------------------------------

    print("  [4/9] Aggregating IXP traffic...")
    ixp_traffic = get_ixp_traffic(
        country_code
    )

    # --------------------------------------------------------
    # PeeringDB — Shared IXP fetch (sections 3 + 4)
    # Single fetch used by peering participation AND CDN presence
    # to avoid redundant API calls and reduce rate-limit risk.
    # --------------------------------------------------------

    active_asns = ripestat.get("country_asn_inventory", {}).get("asns", [])
    total_active_asns = ripestat.get("asn_landscape", {}).get("routed_asns", 0)

    try:
        _, shared_netixlans = _fetch_ixp_netixlans(country_code)
    except Exception as e:
        shared_netixlans = None
        _shared_fetch_error = str(e)
    else:
        _shared_fetch_error = None

    # --------------------------------------------------------
    # PeeringDB — Peering Participation (3.1, 3.2)
    # --------------------------------------------------------

    print("  [5/9] Calculating peering participation...")
    peering_participation = get_peering_participation(
        country_code,
        active_asns=active_asns,
        total_active_asns=total_active_asns,
        netixlans=shared_netixlans
    )

    # Propagate shared fetch error if function received no data
    if shared_netixlans is None and peering_participation.get("status") != "error":
        peering_participation["status"] = "error"
        peering_participation["error"] = _shared_fetch_error

    # --------------------------------------------------------
    # PeeringDB — Global CDN Presence (4.1)
    # --------------------------------------------------------

    print("  [6/9] Checking global CDN presence at IXPs...")
    cdn_presence = get_cdn_presence(
        country_code,
        netixlans=shared_netixlans
    )

    # Propagate shared fetch error if function received no data
    if shared_netixlans is None and cdn_presence.get("status") != "error":
        cdn_presence["status"] = "error"
        cdn_presence["error"] = _shared_fetch_error

    # --------------------------------------------------------
    # PeeringDB — On-Net Caching Nodes (4.2)
    # --------------------------------------------------------

    print("  [7/9] Discovering on-net caching nodes...")
    on_net_caching = get_on_net_caching_nodes(
        country_code
    )

    # --------------------------------------------------------
    # ISOC Pulse — Localization Ratio (4.3)
    # --------------------------------------------------------

    print("  [8/9] Retrieving localization ratio from ISOC Pulse...")
    localization_ratio = get_localization_ratio(
        country_code
    )

    # --------------------------------------------------------
    # RIPE Atlas — Domestic Tromboning (5.1)
    # --------------------------------------------------------

    print("  [9/9] Performing RIPE Atlas traceroutes for domestic tromboning & latency...")
    domestic_tromboning = get_domestic_tromboning(
        country_code
    )

    # --------------------------------------------------------
    # RIPE Atlas — Eyeball Latency to Edge Content (5.2)
    # --------------------------------------------------------

    edge_latency = get_eyeball_latency(
        country_code
    )

    print("  [OK] All peering metrics gathered successfully!")

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
        ixp_traffic,
        peering_participation,
        cdn_presence,
        on_net_caching,
        localization_ratio,
        domestic_tromboning,
        edge_latency
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
        "PeeringDB",
        "ISOC Pulse API",
        "RIPE Atlas"
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

        "peering_participation": peering_participation,

        # ====================================================
        # 4. CONTENT LOCALIZATION & CDNs
        # ====================================================

        "content_localization": {

            "global_cdn_presence": cdn_presence,

            "onnet_caching_nodes": on_net_caching,

            "localization_ratio": localization_ratio
        },

        # ====================================================
        # 5. ROUTING / PERFORMANCE
        # ====================================================

        "routing_performance": {

            "domestic_tromboning": domestic_tromboning,

            "edge_content_latency": edge_latency,

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