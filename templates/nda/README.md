# Template NDA - Accord de Confidentialité

## Variantes

| Type | Fichier | Objet | Non-Sollicitation | Format Partie 2 |
|------|---------|-------|-------------------|-----------------|
| `master` | NDA_Master.docx | Conseil IA générique | ❌ Non | Détaillé (forme juridique, capital) |
| `dev_plateforme` | NDA_DevPlateforme.docx | Dev plateforme ForgeAI | ✅ Oui (12 mois) | Simplifié |
| `prestations` | NDA_Prestations.docx | Missions clients FR Digital | ✅ Oui (12 mois) | Simplifié |

## Différences Structurelles

### Section "ATTENDU QUE"

**master** :
> Dans le cadre le projet de prestations de conseil en intelligence artificielle générative (ci-après, le « Projet »)...

**dev_plateforme** :
> Dans le cadre de la création et de la mise à jour de la plateforme de développement en intelligence artificielle générative dénommée ForgeAI (ci-après, le « Projet »), incluant la conception, le développement, l'amélioration, le déploiement et la maintenance de la plateforme ainsi que des outils et méthodes associés...

**prestations** :
> Dans le cadre de missions de prestations de services pour les clients de FR DIGITAL, nous utilisons la plateforme de développement en intelligence artificielle générative dénommée ForgeAI...

### Section Définitions

**master** : Sans numérotation (« affiliation », « Informations confidentielles », « Représentants »)

**dev_plateforme / prestations** : Avec numérotation (1.1, 1.2, 1.3)

### Bloc Partie 2

**master** (format détaillé) :
```
XXXXX, société par actions simplifiée unipersonnelle, dont le siège social
est situé à XXXXX (France), au capital de XXXXX €, inscrit au registre du
commerce de XXXXX sous le numéro d'inscription XXXXX, dûment représenté par XXXXX,
```

**dev_plateforme / prestations** (format simplifié) :
```
XXXXXXX, dont le siège social est situé à XXXXXXX, inscrit au registre du
commerce de XXX sous le numéro d'inscription XXXXXXX, dûment représenté par XXXXX,
```

## Variables à Injecter

### Partie 1 (FR Digital - fixe)
Déjà renseigné dans tous les templates, pas de remplacement nécessaire.

### Partie 2 (Partenaire - via Pappers)

| Variable | Champ Pappers | Exemple |
|----------|---------------|---------|
| `{{P2_RAISON_SOCIALE}}` | Dénomination | NEXANS |
| `{{P2_FORME_JURIDIQUE}}` | Forme juridique | société anonyme |
| `{{P2_ADRESSE}}` | Siège social | Courbevoie (France) |
| `{{P2_CAPITAL}}` | Capital social | 44 551 877 € |
| `{{P2_VILLE_RCS}}` | Greffe | Nanterre |
| `{{P2_SIREN}}` | SIREN | 393 525 852 |
| `{{P2_REPRESENTANT_NOM}}` | Dirigeant | Christopher Guérin |
| `{{P2_REPRESENTANT_FONCTION}}` | Fonction | Directeur Général |

### Variables Utilisateur

| Variable | Type | Défaut |
|----------|------|--------|
| `{{OBJET_PROJET}}` | texte | Selon variante |
| `{{DUREE_CONFIDENTIALITE}}` | int | 4 (ans) |
| `{{DUREE_NON_SOLLICITATION}}` | int | 12 (mois) |
| `{{LIEU_SIGNATURE}}` | string | Sartrouville |
| `{{DATE_SIGNATURE}}` | date | JJ/MM/AAAA |

## Clauses Conditionnelles

### Article 6 - Non-Sollicitation

Présent uniquement si `clause_non_sollicitation: true`
```
Clause de Non-Sollicitation :

6.1 Le PARTENAIRE s'engage, pendant la durée du Projet et pour une période
de {{DUREE_NON_SOLLICITATION}} mois après la fin du Projet, à ne pas solliciter,
démarcher ou tenter de démarcher directement ou indirectement les clients de
FR DIGITAL...
```

## Usage CLI
```bash
# NDA master (conseil générique, sans non-sollicitation)
python -m src.cli nda \
  --party "393525852" \
  --type master

# NDA dev plateforme (avec non-sollicitation)
python -m src.cli nda \
  --party "393525852" \
  --type dev_plateforme

# NDA prestations clients
python -m src.cli nda \
  --party "393525852" \
  --type prestations \
  --duree-non-sollicitation 18
```
