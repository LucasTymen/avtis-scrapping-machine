#!/usr/bin/env python3
# process_all.py

import os
import sys
import datetime
import logging
import argparse
from config import LOG_DIR  # Import centralised log path

# Import processing modules
from process.merge_csvs import merge_csvs
from process.compare_blacklist import filter_blacklist
from process.enrich_local import enrich_leads
from process.export_output import export_clean_data

# Argument parser for CLI options
parser = argparse.ArgumentParser(description="AVTIS Lead Processing Pipeline")
parser.add_argument("--debug", action="store_true", help="Show debug output in console")
args = parser.parse_args()

# Setup logging
log_filename = f"run_{datetime.date.today()}.log"
log_file = os.path.join(LOG_DIR, log_filename)
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_and_print(message, level="info"):
    """Unified logging and optional printing."""
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    
    if args.debug:
        print(f"[{level.upper()}] {message}")

def main():
    print("\n🔧 Starting AVTIS Scrapping Machine v2")
    print("======================================")

    log_and_print("🚀 AVTIS Lead Processing Started")

    # STEP 1: Merge CSVs from /sheets/
    try:
        log_and_print("📥 Step 1: Merging CSVs from /sheets")
        merged_df = merge_csvs()
    except Exception as e:
        log_and_print(f"❌ Error during merge_csvs(): {e}", level="error")
        sys.exit(1)

    # STEP 2: Filter via blacklist
    try:
        log_and_print("⛔ Step 2: Filtering with blacklist")
        filtered_df = filter_blacklist(merged_df)
    except Exception as e:
        log_and_print(f"❌ Error during filter_blacklist(): {e}", level="error")
        sys.exit(1)

    # STEP 3: Local enrichment
    try:
        log_and_print("🧪 Step 3: Enriching leads locally")
        enriched_df = enrich_leads(filtered_df)
    except Exception as e:
        log_and_print(f"❌ Error during enrich_leads(): {e}", level="error")
        enriched_df = filtered_df  # Fallback: continue without enrichment

    # STEP 4: Export final result
    try:
        log_and_print("📤 Step 4: Exporting to /output")
        export_clean_data(enriched_df)
    except Exception as e:
        log_and_print(f"❌ Error during export_clean_data(): {e}", level="error")
        sys.exit(1)

    log_and_print("✅ AVTIS Lead Processing Complete")
    print("✅ Process finished. Output ready.\n")

if __name__ == "__main__":
    main()
