import concurrent.futures
import os
import socket

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

def get_top_crux_domains(country_code: str, limit: int = 1000) -> list:
    try:
        client = bigquery.Client()
        cc = country_code.lower()
        
        # Query the country-specific CRUX dataset to get the top URLs accessed by users in that country.
        # We filter for the country's TLD to assess national web readiness.
        query = f"""
            SELECT origin
            FROM `chrome-ux-report.country_{cc}.202310`
            WHERE origin LIKE '%.{cc}' OR origin LIKE '%.{cc}/%'
            ORDER BY experimental.popularity.rank ASC
            LIMIT {limit * 3}
        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        domains = []
        for row in results:
            domain = row.origin.replace("https://", "").replace("http://", "").split("/")[0]
            if domain not in domains:
                domains.append(domain)
            if len(domains) >= limit:
                break
                
        return domains
        
    except Exception as e:
        print(f"CRUX Query Error: {e}")
        return []

def check_ipv6_support(domain: str) -> bool:
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        return len(results) > 0
    except Exception:
        return False

def get_crux_web_readiness(country_code: str, limit: int = 1000) -> dict:
    domains = get_top_crux_domains(country_code, limit)
    
    if not domains:
        return {"error": "Failed to fetch domains from CRUX."}
        
    ipv6_capable = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_domain = {executor.submit(check_ipv6_support, dom): dom for dom in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            if future.result():
                ipv6_capable += 1

    ipv4_only = len(domains) - ipv6_capable
    
    return {
        "total_domains": len(domains),
        "ipv6_capable": ipv6_capable,
        "ipv4_only": ipv4_only,
        "ipv6_percentage": round((ipv6_capable / len(domains)) * 100, 1) if len(domains) > 0 else 0
    }
