# Contract Generator

Générateur automatisé de contrats juridiques à partir d'informations sociétés.

## Sources de Données

Le système récupère automatiquement les informations d'entreprises via :

1. **Données de test** (FR Digital, Nexans) - Aucune configuration requise
2. **API SIRENE (INSEE)** - Données officielles du gouvernement français
   - Gratuit avec inscription : https://api.insee.fr/catalogue/
   - TODO: Ajouter la clé API dans `config/settings.yaml`
3. **Saisie manuelle** - Fallback si aucune source automatique disponible

**SIRENs de test disponibles :**
- FR Digital : `901995308`
- Nexans : `393525852`

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
│   ├── scraper.py               # Récupération données via API SIRENE
│   ├── generator.py             # Génération DOCX
│   └── cli.py                   # Interface ligne de commande
└── output/                      # Contrats générés
```

## Architecture

1. **Input** : SIREN ou URL Pappers
2. **Data Retrieval** : API SIRENE (INSEE) ou données de test
3. **Generator** : Application template DOCX + variables
4. **Output** : Contrat DOCX prêt à signer

## Ajouter un nouveau template

1. Créer dossier `templates/[nom]/`
2. Ajouter `config.yaml` avec variables et options
3. Ajouter fichiers `.docx` exemples
4. Documenter dans `README.md` du dossier
