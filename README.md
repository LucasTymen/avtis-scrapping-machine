![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/github/license/LucasTymen/avtis-scrapping-machine)
![GitHub last commit](https://img.shields.io/github/last-commit/LucasTymen/avtis-scrapping-machine)


# 📊 AVTIS Lead Scrapping Machine v2

Cette machine traite automatiquement des fichiers CSV exportés de LinkedIn via PhantomBuster, les nettoie, les enrichit localement, et sort un fichier final prêt pour le CRM ou la prospection manuelle.

---

## ⚙️ Structure du projet

avtisDataOps/ ├── sheets/ # 📥 Fichiers CSV à traiter (exports brut de PhantomBuster) ├── blacklists/ # ⛔ Emails, entreprises ou domaines à exclure ├── staging/ # 🧪 Fichiers tampon pour enrichissement local ├── output/ # 📤 Résultat final (leads_final.csv) ├── logs/ # 📝 Fichiers de log ├── process/ # 🧠 Scripts de traitement (modulaires) ├── process_all.py # 🚀 Script principal de traitement ├── config.py # 🧭 Variables de config centralisées ├── requirements.txt # 📦 Dépendances Python └── README.md # 📖 Ce fichier


---

## 🔄 Comment ça fonctionne

```bash
# Installation
pip install -r requirements.txt

# Lancement du process complet
python3 process_all.py --debug

🧠 Étapes du process :

    Fusion de tous les fichiers .csv depuis sheets/

    Nettoyage des doublons et lignes vides

    Filtrage via blacklist (entreprises, domaines, emails)

    Enrichissement local avec whatweb + whois

    Export final dans output/leads_final.csv

✨ Résultat attendu

Le fichier final contiendra :

    Les colonnes de base (format PhantomBuster)

    inBlacklist (TRUE/FALSE)

    excluded_reason

    techStack (résultat whatweb)

    whois_owner (résultat whois)

    enriched (TRUE/FALSE)

🛠️ Dépendances système

Assure-toi d’avoir installé ces outils CLI :

sudo apt install whois whatweb curl dnsutils -y

✅ Prêt pour prod

    Zéro API externe

    100% local & sécurisé

    Plug & play

    Facilement extensible

    🧠 Créé par Lucas Tymen 🚀