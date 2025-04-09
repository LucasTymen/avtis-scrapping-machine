# compare_blacklist.py

import os
import pandas as pd
import logging
from config import (
    BLACKLIST_DIR,
    COLUMN_EMAIL,
    COLUMN_COMPANY,
    COLUMN_DOMAIN,
    COL_BLACKLISTED,
    COL_EXCLUDED_REASON
)

def load_blacklists():
    """
    Load all CSV files from the blacklists directory and extract known
    emails, companies, and domains into sets for filtering.
    """
    blacklisted_emails = set()
    blacklisted_companies = set()
    blacklisted_domains = set()

    if not os.path.exists(BLACKLIST_DIR):
        logging.warning(f"⚠️ Blacklist folder '{BLACKLIST_DIR}' not found.")
        return blacklisted_emails, blacklisted_companies, blacklisted_domains

    for file in os.listdir(BLACKLIST_DIR):
        if not file.endswith(".csv"):
            continue
        path = os.path.join(BLACKLIST_DIR, file)
        try:
            df = pd.read_csv(path)
            df.columns = [col.strip().lower() for col in df.columns]

            for col in df.columns:
                if "email" in col:
                    blacklisted_emails.update(df[col].dropna().str.lower().str.strip())
                elif "company" in col or "entreprise" in col:
                    blacklisted_companies.update(df[col].dropna().str.lower().str.strip())
                elif "domain" in col:
                    blacklisted_domains.update(df[col].dropna().str.lower().str.strip())
        except Exception as e:
            logging.warning(f"[WARN] Failed to read blacklist file '{file}': {e}")

    return blacklisted_emails, blacklisted_companies, blacklisted_domains


def filter_blacklist(df, blacklists=None):
    """
    Tag each row based on known blacklists and return a filtered DataFrame.
    Adds inBlacklist and excluded_reason columns.
    """
    if blacklists is None:
        blacklists = load_blacklists()

    emails_set, companies_set, domains_set = blacklists

    # Normalize key columns safely
    df["email_norm"] = df[COLUMN_EMAIL].fillna("").str.lower().str.strip() if COLUMN_EMAIL in df.columns else ""
    df["company_norm"] = df[COLUMN_COMPANY].fillna("").str.lower().str.strip() if COLUMN_COMPANY in df.columns else ""
    df["domain_norm"] = df[COLUMN_DOMAIN].fillna("").str.lower().str.strip() if COLUMN_DOMAIN in df.columns else ""

    # Vectorized matching
    df[COL_BLACKLISTED] = (
        df["email_norm"].isin(emails_set) |
        df["company_norm"].isin(companies_set) |
        df["domain_norm"].isin(domains_set)
    )

    # Reason tracking
    df[COL_EXCLUDED_REASON] = ""
    if emails_set:
        df.loc[df["email_norm"].isin(emails_set), COL_EXCLUDED_REASON] += "Blacklisted email; "
    if companies_set:
        df.loc[df["company_norm"].isin(companies_set), COL_EXCLUDED_REASON] += "Blacklisted company; "
    if domains_set:
        df.loc[df["domain_norm"].isin(domains_set), COL_EXCLUDED_REASON] += "Blacklisted domain; "

    # Clean intermediate columns
    df.drop(columns=["email_norm", "company_norm", "domain_norm"], inplace=True)

    # Filter out blacklisted rows
    filtered_df = df[df[COL_BLACKLISTED] == False].copy()
    filtered_df.reset_index(drop=True, inplace=True)

    logging.info(f"⛔ Blacklist filtering done — {len(df) - len(filtered_df)} rows removed.")
    return filtered_df
