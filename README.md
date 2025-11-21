# Contract Generator

Générateur automatisé de contrats juridiques à partir d'informations sociétés (Pappers).

## Quick Start

### Mode Interactif (Recommandé)
```bash
# Lancer le script interactif
./run.sh
```

Le script interactif vous guide à travers :
- Vérification et installation des dépendances
- Sélection du type de NDA
- Saisie des informations de la société
- Génération automatique du contrat

### Mode Ligne de Commande
```bash
# Installation
pip install -r requirements.txt

# Générer un NDA
python -m src.cli nda \
  --party "https://www.pappers.fr/entreprise/nexans-393525852" \
  --type master

# Avec SIREN directement
python -m src.cli nda --party "393525852" --type dev_plateforme
```

## Templates Disponibles

| Template | Statut | Description |
|----------|--------|-------------|
| NDA | ✅ | Accord de confidentialité bi/multi-parties |
| Prestation | 🔜 | Contrat de prestation de services |
| CGV SaaS | 🔜 | Conditions générales de vente |

## Structure du Projet

```
contract-generator/
├── README.md                    # Quick start utilisateur
├── INSTRUCTIONS.md              # Guide architecture pour agent
├── requirements.txt             # Dépendances Python
├── config/
│   └── settings.yaml            # Configuration globale (Pappers API, etc.)
├── templates/
│   └── nda/
│       ├── README.md            # Doc usage NDA (CLI, variables)
│       ├── INSTRUCTIONS.md      # Instructions spécifiques agent NDA
│       ├── config.yaml          # Configuration variantes NDA
│       └── examples/
│           ├── NDA_Master.docx
│           ├── NDA_DevPlateforme.docx
│           └── NDA_Prestations.docx
├── src/
│   ├── models.py                # Modèles de données (Société, etc.)
│   ├── scraper.py               # Scraping Pappers
│   ├── generator.py             # Génération DOCX
│   └── cli.py                   # Interface ligne de commande
└── output/                      # Contrats générés
```

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
