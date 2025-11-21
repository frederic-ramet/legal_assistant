# Instructions Agent - Template NDA

## Contexte

Ce template génère des accords de confidentialité bilatéraux pour FR Digital.
3 variantes existent avec des différences structurelles importantes.

---

## Analyse des Templates Source

### Différences entre variantes

| Élément | master | dev_plateforme | prestations |
|---------|--------|----------------|-------------|
| Format bloc Partie 2 | Détaillé | Simplifié | Simplifié |
| Numérotation définitions | Non (pas de 1.1, 1.2) | Oui | Oui |
| Article 6 Non-Sollicitation | Absent | Présent | Présent |
| Paragraphe définition infos confidentielles | Court | Long (avec exemples) | Long (avec exemples) |

### Placeholders dans les DOCX

Les templates utilisent des placeholders texte brut, pas des balises :
```
XXXXXXX  → raison sociale (7 X)
XXXXX    → valeurs diverses (5 X)
XXX      → ville RCS courte (3 X)
```

**Attention** : Ces placeholders apparaissent plusieurs fois. Utiliser remplacement global.

---

## Bloc Partie 2 - Deux Formats

### Format DETAILED (master)
```
XXXXX, société par actions simplifiée unipersonnelle, dont le siège social
est situé à XXXXX (France), au capital de XXXXX €, inscrit au registre du
commerce de XXXXX sous le numéro d'inscription XXXXX, dûment représenté par XXXXX,
```

**Remplacements** :
1. `XXXXX, société par actions` → `{{raison_sociale}}, {{forme_juridique}}`
2. `situé à XXXXX (France)` → `situé à {{adresse}}`
3. `capital de XXXXX €` → `capital de {{capital}}`
4. `commerce de XXXXX sous` → `commerce de {{ville_rcs}} sous`
5. `numéro d'inscription XXXXX` → `numéro d'inscription {{siren}}`
6. `représenté par XXXXX,` → `représenté par {{representant_nom}},`

### Format SIMPLE (dev_plateforme, prestations)
```
XXXXXXX, dont le siège social est situé àXXXXXXX, inscrit au registre du
commerce de XXX sous le numéro d'inscription XXXXXXX, dûment représenté par XXXXX,
```

**Note** : Pas d'espace après "à" dans le template original (`situé àXXXXXXX`).

**Remplacements** :
1. Premier `XXXXXXX,` → `{{raison_sociale}},`
2. `àXXXXXXX,` → `à {{adresse}},`
3. `commerce de XXX` → `commerce de {{ville_rcs}}`
4. `inscription XXXXXXX,` → `inscription {{siren}},`
5. `par XXXXX,` → `par {{representant_nom}},`

---

## Gestion Article 6 (Non-Sollicitation)

### Variante master
L'article 6 **n'existe pas**. La numérotation va directement :
- Article 5 : Accusé de réception
- Article 6 : Violation (numéroté 6 dans le doc, pas 7)
- Article 7 : Durée
- etc.

### Variantes dev_plateforme / prestations
L'article 6 existe avec le texte complet.

**Stratégie recommandée** :
- NE PAS modifier les templates existants pour ajouter/supprimer l'article 6
- Utiliser le bon template source selon la variante demandée
- Si besoin de modifier la durée non-sollicitation (12 mois par défaut), remplacer dans le texte

---

## Mapping Pappers → Variables

### Champs à extraire de Pappers

| Champ Pappers | Variable | Exemple FR Digital |
|---------------|----------|-------------------|
| `denomination` | raison_sociale | FR DIGITAL |
| `forme_juridique` | forme_juridique | Société par actions simplifiée |
| `siege.adresse` | adresse | Sartrouville (France) |
| `capital` | capital | 5 000 € |
| `greffe` | ville_rcs | Versailles |
| `siren` | siren | 901 995 308 |
| `dirigeants[0].nom` | representant_nom | Frédéric Ramet |
| `dirigeants[0].fonction` | representant_fonction | Président |

### Formatage

- **Capital** : Ajouter espace milliers + `€` (ex: `5 000 €`, `44 551 877 €`)
- **SIREN** : Format avec espaces `XXX XXX XXX`
- **Adresse** : Extraire ville + `(France)` si FR

---

## Section ATTENDU QUE

Chaque variante a un texte différent. Le texte est déjà dans les templates, pas de remplacement nécessaire SAUF si l'utilisateur veut personnaliser l'objet.

Si personnalisation demandée, chercher et remplacer le bloc complet entre "ATTENDU QUE :" et "IL EST ENTENDU".

---

## Signatures

Le bloc signature est un tableau Word :
```
+-----------------------------------+-----------------------------------+
| LE PARTENAIRE                     | FR DIGITAL                        |
+===================================+===================================+
| Nom :                             | Nom : Frédéric Ramet              |
|                                   |                                   |
| Titre :                           | Titre : Président                 |
+-----------------------------------+-----------------------------------+
```

**Remplacements partie 2** :
- Après `Nom :` → `{{representant_nom}}`
- Après `Titre :` → `{{representant_fonction}}`

---

## Implémentation Recommandée

### Approche 1 : Remplacement texte brut (simple)
```python
def replace_placeholders(doc_text, party_data, variant):
    if variant == 'master':
        # Format détaillé - remplacements séquentiels
        ...
    else:
        # Format simple
        ...
```

**Avantage** : Fonctionne avec les templates tels quels
**Inconvénient** : Fragile si structure change

### Approche 2 : Templates avec vrais placeholders (robuste)

Créer des copies des templates avec placeholders explicites `{{variable}}`, puis utiliser docxtpl.

**Avantage** : Plus propre, maintenable
**Inconvénient** : Travail initial de conversion

### Recommandation

Commencer par **Approche 1** pour le POC, migrer vers **Approche 2** si ça fonctionne.

---

## Tests

### Sociétés test Pappers
```
FR Digital : 901995308 (SASU, petit capital)
Nexans : 393525852 (SA, gros capital, multi-dirigeants)
```

### Cas à tester

1. NDA master FR Digital ↔ Nexans
2. NDA dev_plateforme FR Digital ↔ Nexans
3. NDA prestations FR Digital ↔ Nexans
4. Vérifier formatage capital (5 000 € vs 44 551 877 €)
5. Vérifier SIREN avec/sans espaces
