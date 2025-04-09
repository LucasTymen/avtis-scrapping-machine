# merge_csvs.py

import os
import pandas as pd
import tldextract  # pour extraire le domaine depuis une URL
from config import SHEETS_DIR, COLUMN_PROFILE, COLUMN_COMPANY, COLUMN_DOMAIN, COLUMN_EMAIL

def merge_csvs():
    """
    Merge all CSV files from the sheets/ folder into a single pandas DataFrame.
    - Nettoie les colonnes et les lignes vides
    - Supprime les doublons
    - Garantit la présence des colonnes 'company' et 'companyDomain'
    """

    # 🔍 Récupère tous les fichiers CSV dans le dossier sheets/
    all_files = [f for f in os.listdir(SHEETS_DIR) if f.endswith(".csv")]

    if not all_files:
        raise Exception(f"No CSV files found in {SHEETS_DIR}/")

    merged_df = pd.DataFrame()

    # 📥 Fusion des fichiers CSV un par un
    for file in all_files:
        file_path = os.path.join(SHEETS_DIR, file)
        try:
            df = pd.read_csv(file_path)

            # Nettoie les noms de colonnes (supprime les espaces)
            df.columns = [col.strip() for col in df.columns]

            # Supprime les lignes totalement vides
            df.dropna(how="all", inplace=True)

            # Ajoute au DataFrame fusionné
            merged_df = pd.concat([merged_df, df], ignore_index=True)

        except Exception as e:
            print(f"[WARN] Failed to read {file}: {e}")

    # 🔁 Suppression des doublons par URL de profil LinkedIn
    if COLUMN_PROFILE in merged_df.columns:
        merged_df.drop_duplicates(subset=[COLUMN_PROFILE], inplace=True)
    else:
        merged_df.drop_duplicates(inplace=True)

    # ✅ Normalisation de la colonne 'company'
    if COLUMN_COMPANY not in merged_df.columns:
        if "Current company" in merged_df.columns:
            merged_df[COLUMN_COMPANY] = merged_df["Current company"]
        elif "companyName" in merged_df.columns:
            merged_df[COLUMN_COMPANY] = merged_df["companyName"]
        else:
            merged_df[COLUMN_COMPANY] = ""

    # 🌐 Création de la colonne 'companyDomain' si absente
    if COLUMN_DOMAIN not in merged_df.columns:
        # On tente d'extraire depuis 'linkedinCompanyUrl'
        if "linkedinCompanyUrl" in merged_df.columns:
            def extract_domain(url):
                try:
                    ext = tldextract.extract(url)
                    return ".".join(part for part in [ext.domain, ext.suffix] if part)
                except:
                    return ""
            merged_df[COLUMN_DOMAIN] = merged_df["linkedinCompanyUrl"].fillna("").apply(extract_domain)
        else:
            merged_df[COLUMN_DOMAIN] = ""

    # 🔁 Fallback : si domaine vide, on l'extrait depuis l'email
    if COLUMN_EMAIL in merged_df.columns:
        def fallback_from_email(row):
            if not row[COLUMN_DOMAIN] and pd.notna(row[COLUMN_EMAIL]) and "@" in row[COLUMN_EMAIL]:
                return row[COLUMN_EMAIL].split("@")[-1].strip().lower()
            return row[COLUMN_DOMAIN]
        merged_df[COLUMN_DOMAIN] = merged_df.apply(fallback_from_email, axis=1)

    # 🔄 Réinitialise l’index final
    merged_df.reset_index(drop=True, inplace=True)

    return merged_df
