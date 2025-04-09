# export_output.py

import os
import pandas as pd
import logging
from config import OUTPUT_FILE, OUTPUT_DIR

def export_clean_data(df):
    """
    Export the final DataFrame to the output directory as a CSV file.
    Encoding: UTF-8 with BOM (utf-8-sig) for Excel compatibility.
    """
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        logging.info(f"✅ Exported {len(df)} rows to {OUTPUT_FILE}")
        print(f"📦 Output saved to {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"❌ Failed to export output: {e}")
        print(f"[ERROR] Could not save output: {e}")
