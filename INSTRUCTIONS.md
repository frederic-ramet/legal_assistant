# Instructions Agent - Contract Generator

## Vue d'ensemble

Générateur de contrats juridiques FR.
- **Input** : URL Pappers ou SIREN
- **Process** : Scraping + templating DOCX
- **Output** : Contrat prêt à signer

---

## Architecture Générale

### 1. Scraper (`src/scraper.py`)

Extraction données société depuis Pappers.

**Input** : URL ou SIREN
```
https://www.pappers.fr/entreprise/fr-digital-901995308
ou
901995308
```

**Output** : Dataclass `Societe`

**Méthode** : Scraping HTML (BeautifulSoup), pas d'API payante.

**Fallback** : Si échec extraction, permettre saisie manuelle.

### 2. Models (`src/models.py`)

Dataclass commune tous templates :
```python
@dataclass
class Societe:
    siren: str
    raison_sociale: str
    forme_juridique: str
    capital: str              # Formaté : "5 000 €"
    adresse: str
    ville_rcs: str
    representant_nom: str
    representant_fonction: str
```

### 3. Generator (`src/generator.py`)

Moteur de templating générique.

**Responsabilités** :
- Charger config template (`config.yaml`)
- Appliquer variables au DOCX
- Gérer clauses conditionnelles
- Produire output

**Libs recommandées** : `python-docx` ou `docxtpl`

### 4. CLI (`src/cli.py`)

Interface ligne de commande.
```bash
python -m src.cli [template] [options]
```

Chaque template définit ses options dans son `config.yaml`.

---

## Organisation Templates

Chaque template = 1 dossier dans `templates/` :
```
templates/[nom]/
├── README.md           # Doc utilisateur (usage, CLI)
├── INSTRUCTIONS.md     # Instructions agent (implémentation)
├── config.yaml         # Variables, variantes, defaults
└── examples/           # Fichiers DOCX source
```

**Important** : Lire le `INSTRUCTIONS.md` du template avant d'implémenter.

---

## Conventions

### Nommage Output
```
[TYPE]_[Variante]_[Partie1]_[Partie2]_[Date].docx
```
Exemple : `NDA_master_FRDigital_Nexans_21-11-2025.docx`

### Formatage FR
- Dates : `JJ/MM/AAAA`
- Montants : `X XXX €` (espace milliers)
- SIREN : `XXX XXX XXX`

### Logs
Afficher clairement :
- Données extraites de Pappers
- Variables appliquées
- Fichier généré

---

## Workflow Développement

1. **Lire** `templates/[nom]/INSTRUCTIONS.md`
2. **Analyser** les exemples DOCX
3. **Implémenter** scraper si nouveaux champs requis
4. **Créer** logique de remplacement spécifique
5. **Tester** sur sociétés variées

---

## Extension

Pour ajouter un nouveau template :

1. Créer structure dossier
2. Analyser les DOCX source, documenter les placeholders
3. Écrire `config.yaml` avec variables
4. Écrire `INSTRUCTIONS.md` avec détails implémentation
5. Le generator détecte automatiquement via config

---

## Priorité Actuelle

**Template NDA** : Voir `templates/nda/INSTRUCTIONS.md` pour les détails d'implémentation spécifiques (formats bloc partie 2, gestion article 6, placeholders DOCX).
