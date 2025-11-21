# Instructions Agent - Contract Generator

## Contexte

Générateur de contrats juridiques FR. Scraping Pappers + templating DOCX.

## Principes Architecture

### 1. Modularité

Chaque type de contrat = 1 dossier dans `templates/`
```
templates/[type]/
├── README.md      # Doc usage
├── config.yaml    # Variables, options, clauses
└── examples/      # Fichiers DOCX source
```

### 2. Données Société

Dataclass commune pour toutes les sociétés :
```python
@dataclass
class Societe:
    siren: str
    raison_sociale: str
    forme_juridique: str      # SAS, SARL, etc.
    capital: str              # "5 000 €"
    adresse: str
    ville_rcs: str            # Versailles, Paris, etc.
    representant_nom: str
    representant_fonction: str  # Président, Gérant, etc.
```

### 3. Scraper Pappers

- Input : URL ou SIREN
- Parser HTML (BeautifulSoup)
- Fallback : saisie manuelle si échec
- Cache local JSON optionnel

### 4. Moteur Templating

- Utiliser `python-docx` ou `docxtpl`
- Placeholders format `{{variable}}`
- Gestion clauses conditionnelles via config

### 5. CLI
```bash
python -m src.cli [template] [options]
```

Chaque template définit ses propres arguments dans son `config.yaml`.

## Workflow Développement

1. Lire le README du template ciblé
2. Analyser les exemples DOCX fournis
3. Identifier variables et clauses conditionnelles
4. Implémenter scraper si nouveau champ requis
5. Créer template avec placeholders
6. Tester sur sociétés variées

## Conventions

- Nommage output : `[TYPE]_[Société1]_[Société2]_[Date].docx`
- Dates format FR : `JJ/MM/AAAA`
- Montants : `X XXX €` (espace milliers)
- Logs clairs pour debug

## Extension Future

Pour ajouter un template :
1. Créer structure dossier
2. Documenter variables dans config.yaml
3. Ajouter exemples annotés
4. Le générateur détecte automatiquement les nouveaux templates
