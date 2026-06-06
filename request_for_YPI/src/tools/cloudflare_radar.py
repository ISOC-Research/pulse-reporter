"""
Cloudflare Radar API Client
============================
Provides methods to fetch internet quality and speed data from the
Cloudflare Radar API (https://developers.cloudflare.com/radar/).

Usage:
    from request_for_YPI.src.tools.cloudflare_radar import RadarClient

    client = RadarClient()  # reads CLOUDFLARE_RADAR_API_TOKEN from .env
    data = client.get_speed_summary(country="AU")
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load .env from project root
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
load_dotenv(os.path.join(_root, '.env'))

BASE_URL = "https://api.cloudflare.com/client/v4/radar"


class RadarClient:
    """Thin wrapper around the Cloudflare Radar REST API."""

    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("CLOUDFLARE_RADAR_API_TOKEN")
        if not self.token:
            raise ValueError(
                "No Cloudflare Radar API token found.\n"
                "Set CLOUDFLARE_RADAR_API_TOKEN in your .env file or pass it directly."
            )
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        })

    def _get(self, path: str, params: dict | None = None) -> dict:
        """Make a GET request and return the parsed JSON response."""
        url = f"{BASE_URL}/{path}"
        params = params or {}
        params.setdefault("format", "json")
        resp = self._session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            errors = data.get("errors", [])
            raise RuntimeError(f"Radar API error: {errors}")
        return data.get("result", {})

    # ── Speed Tests ──────────────────────────────────────────────

    def get_speed_summary(self, country: str, date_range: str = "90d") -> dict:
        """
        Get speed test summary for a country.
        Returns download/upload speeds (Mbps) and latency (ms).
        Endpoint: GET /radar/quality/speed/summary
        """
        return self._get("quality/speed/summary", {
            "location": country,
            "dateRange": date_range,
        })

    def get_speed_top_locations(self, metric: str = "downloadSpeed",
                                 date_range: str = "90d", limit: int = 10) -> dict:
        """
        Get top locations ranked by a speed metric.
        metric: downloadSpeed | uploadSpeed | jitter | latency
        Endpoint: GET /radar/quality/speed/top/locations
        """
        return self._get("quality/speed/top/locations", {
            "metric": metric,
            "dateRange": date_range,
            "limit": limit,
        })

    # ── Internet Quality Index (IQI) ────────────────────────────

    def get_iqi_summary(self, country: str, metric: str = "bandwidth",
                        date_range: str = "90d") -> dict:
        """
        Get Internet Quality Index summary for a country.
        metric: bandwidth | latency | dns
        Endpoint: GET /radar/quality/iqi/summary
        """
        return self._get("quality/iqi/summary", {
            "location": country,
            "metric": metric,
            "dateRange": date_range,
        })

    def get_iqi_timeseries(self, country: str, metric: str = "bandwidth",
                           date_range: str = "90d") -> dict:
        """
        Get Internet Quality Index timeseries for a country.
        metric: bandwidth | latency | dns
        Endpoint: GET /radar/quality/iqi/timeseries_groups
        """
        return self._get("quality/iqi/timeseries_groups", {
            "location": country,
            "metric": metric,
            "dateRange": date_range,
        })

    # ── Speed Histogram ─────────────────────────────────────────

    def get_speed_histogram(self, country: str, metric: str = "downloadSpeed",
                            bucket_count: int = 10,
                            date_range: str = "90d") -> dict:
        """
        Get speed distribution histogram for a country.
        Reveals inequality: does everyone get similar speeds or is there
        a wide gap between urban and rural users?
        metric: downloadSpeed | uploadSpeed | latency | jitter
        Endpoint: GET /radar/quality/speed/histogram
        """
        return self._get("quality/speed/histogram", {
            "location": country,
            "metric": metric,
            "bucketCount": bucket_count,
            "dateRange": date_range,
        })

    # ── TCP Resets & Timeouts (Connection Tampering) ─────────────

    def get_tcp_resets_timeouts_summary(self, country: str,
                                        date_range: str = "90d") -> dict:
        """
        Get TCP connection outcome summary for a country.
        Returns the breakdown of connections into: successful, reset, timeout.
        High reset/timeout rates indicate connection tampering, middlebox
        interference, or infrastructure instability.
        Endpoint: GET /radar/tcp_resets_timeouts/summary
        """
        return self._get("tcp_resets_timeouts/summary", {
            "location": country,
            "dateRange": date_range,
        })

    # ── Traffic Anomalies (Outage Detection) ─────────────────────

    def get_traffic_anomalies(self, country: str,
                              date_range: str = "90d",
                              limit: int = 20) -> dict:
        """
        Get detected internet traffic anomalies for a country.
        Anomalies indicate potential outages or infrastructure instability.
        Frequent anomalies point to fragile infrastructure — directly
        relevant to IRI resilience scoring.
        Endpoint: GET /radar/traffic_anomalies/locations
        """
        return self._get("traffic_anomalies/locations", {
            "location": country,
            "dateRange": date_range,
            "limit": limit,
        })
