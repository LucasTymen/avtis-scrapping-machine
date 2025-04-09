# enrich_local.py

import subprocess
import pandas as pd
import logging
from config import COLUMN_DOMAIN, COL_TECHSTACK, COL_WHOIS, COL_ENRICHED

def run_whatweb(domain):
    """
    Execute whatweb command on a given domain to detect tech stack.
    """
    try:
        result = subprocess.run(["whatweb", f"https://{domain}"],
                                capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        logging.warning(f"[whatweb] failed for {domain}: {e}")
        return "whatweb_error"

def run_whois(domain):
    """
    Execute whois command on a domain and extract organization info if available.
    """
    try:
        result = subprocess.run(["whois", domain],
                                capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().splitlines()
        for line in lines:
            if "OrgName" in line or "Organization" in line or "Registrant Name" in line:
                return line.strip()
        return "whois_ok"
    except Exception as e:
        logging.warning(f"[whois] failed for {domain}: {e}")
        return "whois_error"

def enrich_leads(df):
    """
    For each row in the DataFrame, use whatweb + whois to enrich companyDomain.
    Add columns:
        - techStack (result of whatweb)
        - whois_owner (result of whois)
        - enriched (True/False)
    """

    # Check that domain column exists
    if COLUMN_DOMAIN not in df.columns:
        logging.warning(f"No '{COLUMN_DOMAIN}' column found. Skipping enrichment.")
        df[COL_TECHSTACK] = ""
        df[COL_WHOIS] = ""
        df[COL_ENRICHED] = False
        return df

    # Add enrichment columns
    df[COL_TECHSTACK] = ""
    df[COL_WHOIS] = ""
    df[COL_ENRICHED] = False

    for idx, row in df.iterrows():
        domain = str(row[COLUMN_DOMAIN]).strip().lower()

        if not domain or domain == "nan":
            continue

        tech = run_whatweb(domain)
        whois = run_whois(domain)

        df.at[idx, COL_TECHSTACK] = tech
        df.at[idx, COL_WHOIS] = whois
        df.at[idx, COL_ENRICHED] = True

        logging.info(f"[{domain}] ✅ enriched")

    return df
