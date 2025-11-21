# Modèles de données pour les contrats et entreprises

from dataclasses import dataclass
from typing import Optional


@dataclass
class Societe:
    """Modèle de données pour une société."""
    siren: str
    raison_sociale: str
    forme_juridique: str
    capital: str              # Formaté : "5 000 €"
    adresse: str
    ville_rcs: str
    representant_nom: str
    representant_fonction: str

    def __str__(self) -> str:
        return f"{self.raison_sociale} (SIREN: {self.siren})"
