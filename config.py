# config.py

# 🗂️ Dossier racine du projet
ROOT_DIR = "."

# 📥 Dossiers sources
SHEETS_DIR = f"{ROOT_DIR}/sheets"
BLACKLIST_DIR = f"{ROOT_DIR}/blacklists"
STAGING_DIR = f"{ROOT_DIR}/staging"

# 📤 Dossier de sortie
OUTPUT_DIR = f"{ROOT_DIR}/output"
OUTPUT_FILE = f"{OUTPUT_DIR}/leads_final.csv"

# 🧾 Dossier des logs
LOG_DIR = f"{ROOT_DIR}/logs"

# 🧱 Colonnes essentielles attendues
COLUMN_PROFILE = "profileUrl"
COLUMN_COMPANY = "company"
COLUMN_EMAIL = "email"
COLUMN_DOMAIN = "companyDomain"

# 🔍 Colonnes ajoutées par le pipeline
COL_ENRICHED = "enriched"
COL_BLACKLISTED = "inBlacklist"
COL_EXCLUDED_REASON = "excluded_reason"
COL_TECHSTACK = "techStack"
COL_WHOIS = "whois_owner"
