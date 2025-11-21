# Contract Generator

Générateur automatisé de contrats juridiques à partir d'informations sociétés (Pappers).

## Quick Start
```bash
# Installation
pip install -r requirements.txt

# Générer un NDA
python -m src.cli nda \
  --party "https://www.pappers.fr/entreprise/fr-digital-901995308" \
  --party "https://www.pappers.fr/entreprise/nexans-393525852" \
  --type master
```

## Templates Disponibles

| Template | Statut | Description |
|----------|--------|-------------|
| NDA | ✅ | Accord de confidentialité bi/multi-parties |
| Prestation | 🔜 | Contrat de prestation de services |
| CGV SaaS | 🔜 | Conditions générales de vente |

## Architecture

1. **Input** : URL Pappers ou SIREN
2. **Scraper** : Extraction données société
3. **Generator** : Application template + variables
4. **Output** : DOCX téléchargeable

## Ajouter un nouveau template

1. Créer dossier `templates/[nom]/`
2. Ajouter `config.yaml` avec variables et options
3. Ajouter fichiers `.docx` exemples
4. Documenter dans `README.md` du dossier
