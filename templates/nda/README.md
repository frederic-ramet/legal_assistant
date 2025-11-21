# Template NDA (Accord de Non-Divulgation)

## Description
Ce dossier contient les templates et configurations pour générer des NDA personnalisés.

## Exemples disponibles
- `NDA_Master.docx` : Template principal pour NDA standard
- `NDA_DevPlateforme.docx` : Template spécifique pour développement de plateforme
- `NDA_Prestations.docx` : Template pour accords de prestation

## Configuration
Le fichier `config.yaml` définit les variables, options et clauses spécifiques aux NDA.

## Utilisation
Pour générer un NDA, utilisez la commande :
```bash
python src/cli.py generate --type nda --company "Nom de l'entreprise"
```
