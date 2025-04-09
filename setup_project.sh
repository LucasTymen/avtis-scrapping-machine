#!/bin/bash

echo "🛠️  Setting up AVTIS Scrapping Machine project..."

# Set default root folder
ROOT="avtisDataOps"

# Create directory structure
mkdir -p $ROOT/{sheets,blacklists,staging,output,logs,process}
touch $ROOT/{process_all.py,requirements.txt,README.md}
touch $ROOT/staging/enrich_to_compare.csv $ROOT/staging/enrich_result.csv
touch $ROOT/output/leads_final.csv
touch $ROOT/logs/run_$(date +%F).log

# Create empty process module files
touch $ROOT/process/{merge_csvs.py,compare_blacklist.py,enrich_local.py,export_output.py}

# Create config.py
cat <<EOL > $ROOT/config.py
# config.py

ROOT_DIR = "."

SHEETS_DIR = f"{ROOT_DIR}/sheets"
BLACKLIST_DIR = f"{ROOT_DIR}/blacklists"
STAGING_DIR = f"{ROOT_DIR}/staging"
OUTPUT_DIR = f"{ROOT_DIR}/output"
LOG_DIR = f"{ROOT_DIR}/logs"

OUTPUT_FILE = f"{OUTPUT_DIR}/leads_final.csv"

COLUMN_PROFILE = "profileUrl"
COLUMN_COMPANY = "company"
COLUMN_EMAIL = "email"
COLUMN_DOMAIN = "companyDomain"

COL_ENRICHED = "enriched"
COL_BLACKLISTED = "inBlacklist"
COL_EXCLUDED_REASON = "excluded_reason"
COL_TECHSTACK = "techStack"
COL_WHOIS = "whois_owner"
EOL

chmod +x $ROOT/process_all.py
echo "✅ AVTIS project structure created in ./$ROOT/"
