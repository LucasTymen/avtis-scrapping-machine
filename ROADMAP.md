# 🛣️ AVTIS Scrapping Machine – Roadmap

Suivi de développement & idées d'évolution pour industrialiser le traitement des leads AVTIS.

---

## ✅ Fonctionnalités terminées

- [x] Fusion automatique des exports LinkedIn (`sheets/*.csv`)
- [x] Nettoyage des doublons
- [x] Filtrage via blacklist (email / société / domaine)
- [x] Enrichissement local (`whatweb`, `whois`)
- [x] Fallback sur email si le domaine est manquant
- [x] Export propre vers `output/leads_final.csv`
- [x] Script `process_all.py` pour tout automatiser

---

## 🧠 Prochaines améliorations

- [ ] 🔍 Fichier `filter_geo.py` pour exclure par ville / zone
- [ ] 🧪 `sector_matcher.py` pour taguer les leads improbables intéressants
- [ ] 🤖 Intégration `csv_to_lemlist.py` ou `csv_to_airtable.py`
- [ ] 📊 Ajout d’un module de scoring / lead prioritization
- [ ] 🛡️ Validation de domaines MX / vérification d’emails
- [ ] 📥 Webhook d’import automatique depuis PhantomBuster
- [ ] 🌐 Version cloud + dashboard Streamlit ou Gradio

---

## 🚀 Objectif

💡 Faire de ce repo une **machine open-source robuste** pour la qualification, le scoring, et l’export de leads issus de scraping LinkedIn et OSINT, au service de la croissance d’AVTIS.

---

> Maintenu par Lucas Tymen – v2
