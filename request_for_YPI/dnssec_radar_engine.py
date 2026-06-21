"""
dnssec_radar_engine.py

Cloudflare Radar wrapper for DNSSEC report generation.
"""

from request_for_YPI.src.tools.cloudflare_radar import RadarClient


# --------------------------------------------------
# DNS Quality
# --------------------------------------------------

def get_country_dns_quality(country: str):

    client = RadarClient()

    result = client.get_iqi_summary(
        country=country.upper(),
        metric="dns"
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "p25_ms": float(summary.get("p25", 0)),
        "p50_ms": float(summary.get("p50", 0)),
        "p75_ms": float(summary.get("p75", 0))
    }


# --------------------------------------------------
# Latency Quality
# --------------------------------------------------

def get_country_latency_quality(country: str):

    client = RadarClient()

    result = client.get_iqi_summary(
        country=country.upper(),
        metric="latency"
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "p25_ms": float(summary.get("p25", 0)),
        "p50_ms": float(summary.get("p50", 0)),
        "p75_ms": float(summary.get("p75", 0))
    }


# --------------------------------------------------
# Bandwidth Quality
# --------------------------------------------------

def get_country_bandwidth_quality(country: str):

    client = RadarClient()

    result = client.get_iqi_summary(
        country=country.upper(),
        metric="bandwidth"
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "p25": float(summary.get("p25", 0)),
        "p50": float(summary.get("p50", 0)),
        "p75": float(summary.get("p75", 0))
    }


# --------------------------------------------------
# TCP Reliability
# --------------------------------------------------

def get_country_tcp_resets(country: str):

    client = RadarClient()

    result = client.get_tcp_resets_timeouts_summary(
        country=country.upper()
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "connection_success": float(
            summary.get("no_match", 0)
        ),
        "post_syn": float(
            summary.get("post_syn", 0)
        ),
        "post_ack": float(
            summary.get("post_ack", 0)
        ),
        "post_psh": float(
            summary.get("post_psh", 0)
        ),
        "later_in_flow": float(
            summary.get("later_in_flow", 0)
        )
    }


# --------------------------------------------------
# DNSSEC Validation Status (Country)
# --------------------------------------------------

def get_dnssec_validation_status(country: str):

    client = RadarClient()

    result = client._get(
        "dns/summary/DNSSEC",
        {
            "location": country.upper(),
            "dateRange": "7d"
        }
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "secure": float(summary.get("SECURE", 0)),
        "insecure": float(summary.get("INSECURE", 0)),
        "invalid": float(summary.get("INVALID", 0)),
        "other": float(summary.get("OTHER", 0))
    }


# --------------------------------------------------
# Top DNS Query Share by ASN
# --------------------------------------------------

def get_dns_query_distribution_by_asn(country: str):

    client = RadarClient()

    result = client._get(
        "dns/summary/AS",
        {
            "location": country.upper(),
            "dateRange": "7d"
        }
    )

    summary = result.get("summary_0", {})

    asns = []

    for key, value in summary.items():

        if key.lower() == "other":
            continue

        asns.append({
            "asn": int(key),
            "query_share": float(value)
        })

    asns.sort(
        key=lambda x: x["query_share"],
        reverse=True
    )

    return {
        "country": country.upper(),
        "asns": asns
    }


# --------------------------------------------------
# DNSSEC Validation Status by ASN
# --------------------------------------------------

def get_dnssec_validation_by_asn(
    country: str,
    asn: int
):

    client = RadarClient()

    result = client._get(
        "dns/summary/DNSSEC",
        {
            "location": country.upper(),
            "dateRange": "7d",
            "asn": str(asn)
        }
    )

    summary = result.get("summary_0", {})

    return {
        "country": country.upper(),
        "asn": asn,
        "secure": float(summary.get("SECURE", 0)),
        "insecure": float(summary.get("INSECURE", 0)),
        "invalid": float(summary.get("INVALID", 0)),
        "other": float(summary.get("OTHER", 0))
    }

def get_top_asn_dnssec_validation(country: str):

    asn_data = get_dns_query_distribution_by_asn(country)

    results = []

    for item in asn_data["asns"]:

        asn = item["asn"]

        validation = get_dnssec_validation_by_asn(
            country,
            asn
        )

        asn_info = get_asn_details(asn)

        results.append({
            "asn": asn,
            "name": asn_info.get("name"),
            "aka": asn_info.get("aka"),
            "country": asn_info.get("country"),
            "org_name": asn_info.get("orgName"),
            "query_share": item["query_share"],
            "secure": validation["secure"],
            "insecure": validation["insecure"],
            "invalid": validation["invalid"],
            "other": validation["other"]
        })

    results.sort(
        key=lambda x: x["query_share"],
        reverse=True
    )

    return results

def get_asn_details(asn: int):

    client = RadarClient()

    result = client._get(
        f"entities/asns/{asn}"
    )

    return result.get("asn", {})