# Templates DOCX NDA

## Fichiers requis

Ce dossier doit contenir les 3 templates DOCX suivants :

1. **NDA_Master.docx** - Template pour NDA conseil IA générique
2. **NDA_DevPlateforme.docx** - Template pour développement plateforme ForgeAI
3. **NDA_Prestations.docx** - Template pour missions clients FR Digital

## Format des placeholders

Les templates DOCX doivent contenir des placeholders qui seront remplacés par les données réelles :

### Format DETAILED (NDA_Master.docx)

```
XXXXX, société par actions simplifiée unipersonnelle, dont le siège social
est situé à XXXXX (France), au capital de XXXXX €, inscrit au registre du
commerce de XXXXX sous le numéro d'inscription XXXXX, dûment représenté par XXXXX,
```

### Format SIMPLE (NDA_DevPlateforme.docx, NDA_Prestations.docx)

```
XXXXXXX, dont le siège social est situé à XXXXXXX, inscrit au registre du
commerce de XXX sous le numéro d'inscription XXXXXXX, dûment représenté par XXXXX,
```

### Bloc Signatures (tous les templates)

Dans le tableau de signatures :
```
LE PARTENAIRE                     FR DIGITAL
Nom :                             Nom : Frédéric Ramet
Titre :                           Titre : Président
```

## Note

Les fichiers DOCX ne sont pas inclus dans le dépôt Git. Vous devez les ajouter manuellement dans ce dossier avant de pouvoir générer des NDA.

## Test sans fichiers DOCX

Si vous n'avez pas encore les fichiers DOCX, vous pouvez tester le scraper et le CLI :

```bash
# Tester le scraper
python -m src.scraper

# Tester le CLI (affichera une erreur sur le template manquant)
python -m src.cli nda --party "393525852" --type master
```
