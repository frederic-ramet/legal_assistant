# Module pour récupérer les informations d'entreprise via API SIRENE (INSEE)

import re
import requests
from typing import Optional
from .models import Societe


def format_capital(capital_value: float) -> str:
    """Formate le capital avec espaces milliers et €."""
    if capital_value == 0:
        return "0 €"

    capital_str = f"{int(capital_value):,}".replace(',', ' ')
    return f"{capital_str} €"


def format_siren(siren: str) -> str:
    """Formate le SIREN avec espaces (XXX XXX XXX)."""
    siren = siren.replace(' ', '')
    if len(siren) == 9:
        return f"{siren[0:3]} {siren[3:6]} {siren[6:9]}"
    return siren


def extract_siren_from_url(url: str) -> Optional[str]:
    """Extrait le SIREN d'une URL Pappers."""
    # Format: https://www.pappers.fr/entreprise/nom-entreprise-123456789
    match = re.search(r'-(\d{9})$', url)
    if match:
        return match.group(1)
    return None


def get_test_data(siren: str) -> Optional[Societe]:
    """Données de test pour FR Digital et Nexans."""
    test_data = {
        "901995308": Societe(
            siren="901 995 308",
            raison_sociale="FR DIGITAL",
            forme_juridique="Société par actions simplifiée unipersonnelle",
            capital="5 000 €",
            adresse="Sartrouville (France)",
            ville_rcs="Versailles",
            representant_nom="Frédéric Ramet",
            representant_fonction="Président"
        ),
        "393525852": Societe(
            siren="393 525 852",
            raison_sociale="NEXANS",
            forme_juridique="Société anonyme",
            capital="44 551 877 €",
            adresse="Courbevoie (France)",
            ville_rcs="Nanterre",
            representant_nom="Christopher Guérin",
            representant_fonction="Directeur Général"
        )
    }

    siren_clean = siren.replace(' ', '')
    return test_data.get(siren_clean)


def fetch_from_sirene_api(siren: str) -> Optional[Societe]:
    """
    Récupère les données d'une société depuis l'API SIRENE v3.11 (INSEE).

    Note: L'API SIRENE requiert une clé API gratuite.

    Pour obtenir une clé API:
    1. Se connecter sur https://portail-api.insee.fr/
    2. Créer une application (mode "simple")
    3. Souscrire au plan "Public" de l'API Sirene
    4. Récupérer la clé API (X-INSEE-Api-Key-Integration)

    Documentation: https://portail-api.insee.fr/ > API Sirene > Documentation
    État du service: https://www.sirene.fr/sirene/public/accueil
    """
    # Vérifier si une clé API est configurée (future implémentation)
    api_key = None  # TODO: Charger depuis config/settings.yaml

    # URL correcte de l'API SIRENE v3.11
    url = f"https://api.insee.fr/api-sirene/3.11/siren/{siren}"

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Contract-Generator/1.0'
    }

    # La clé API se transmet dans le header X-INSEE-Api-Key-Integration
    if api_key:
        headers['X-INSEE-Api-Key-Integration'] = api_key

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # L'API SIRENE retourne une structure complexe
            unite_legale = data.get('uniteLegale', {})
            periode = unite_legale.get('periodesUniteLegale', [{}])[0]

            # Extraire les données
            raison_sociale = (
                periode.get('denominationUniteLegale', '') or
                periode.get('denominationUsuelle1UniteLegale', '') or
                ''
            )

            forme_juridique = periode.get('categorieJuridiqueUniteLegale', '')

            # Mapping des codes de forme juridique vers des noms complets
            formes_juridiques = {
                '5499': 'Société par actions simplifiée',
                '5710': 'Société par actions simplifiée unipersonnelle',
                '5599': 'Société à responsabilité limitée',
                '5498': 'Société anonyme',
            }
            forme_juridique_nom = formes_juridiques.get(forme_juridique, f"Code {forme_juridique}")

            # Capital social
            capital_raw = periode.get('capitalVariable', '') or periode.get('montantCapitalUniteLegale')
            capital = format_capital(float(capital_raw)) if capital_raw else "Non renseigné"

            # Adresse du siège
            adresse_siege = unite_legale.get('adresseEtablissement', {})
            commune = adresse_siege.get('libelleCommuneEtablissement', '')
            adresse = f"{commune} (France)" if commune else "Non renseigné"

            # RCS (tribunal)
            ville_rcs = commune  # Approximation, l'API ne donne pas directement le greffe

            siren_formatted = format_siren(siren)

            print(f"✅ Données récupérées depuis l'API SIRENE:")
            print(f"   Raison sociale: {raison_sociale}")
            print(f"   Forme juridique: {forme_juridique_nom}")
            print(f"   Capital: {capital}")
            print(f"   Adresse: {adresse}")
            print(f"   SIREN: {siren_formatted}")

            return Societe(
                siren=siren_formatted,
                raison_sociale=raison_sociale,
                forme_juridique=forme_juridique_nom,
                capital=capital,
                adresse=adresse,
                ville_rcs=ville_rcs,
                representant_nom="Non disponible (API SIRENE)",
                representant_fonction="Non disponible"
            )

        elif response.status_code == 403:
            print(f"⚠️  API SIRENE requiert une clé API (gratuite)")
            print(f"   Pour l'obtenir: https://portail-api.insee.fr/")
            return None

        elif response.status_code == 404:
            print(f"⚠️  SIREN {siren} non trouvé dans la base SIRENE")
            return None

        elif response.status_code == 429:
            print(f"⚠️  Rate limit atteint sur l'API SIRENE")
            return None

        else:
            print(f"⚠️  Erreur API SIRENE: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️  Erreur de connexion à l'API SIRENE: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        print(f"⚠️  Erreur de parsing des données SIRENE: {e}")
        return None


def scrape_pappers(identifier: str) -> Societe:
    """
    Récupère les informations d'une société.

    Sources (dans l'ordre) :
    1. Données de test (FR Digital, Nexans)
    2. API SIRENE de l'INSEE (gratuite)
    3. Saisie manuelle

    Args:
        identifier: URL Pappers ou SIREN

    Returns:
        Objet Societe avec les données
    """
    # Extraire le SIREN
    if identifier.startswith('http'):
        siren = extract_siren_from_url(identifier)
        if not siren:
            raise ValueError(f"Impossible d'extraire le SIREN de l'URL: {identifier}")
    else:
        siren = identifier.replace(' ', '')
        if len(siren) != 9:
            raise ValueError(f"SIREN invalide: {siren} (doit contenir 9 chiffres)")

    print(f"📥 Récupération des données pour SIREN {siren}...")

    # 1. Vérifier si c'est une donnée de test
    test_societe = get_test_data(siren)
    if test_societe:
        print(f"ℹ️  Utilisation des données de test")
        return test_societe

    # 2. Essayer l'API SIRENE
    print(f"🔍 Recherche dans l'API SIRENE (INSEE)...")
    sirene_societe = fetch_from_sirene_api(siren)
    if sirene_societe:
        return sirene_societe

    # 3. Fallback : erreur ou saisie manuelle
    print(f"\n❌ Impossible de récupérer les données automatiquement.")
    print(f"   Solutions:")
    print(f"   1. Utiliser un SIREN de test (901995308 ou 393525852)")
    print(f"   2. Obtenir une clé API SIRENE gratuite: https://portail-api.insee.fr/")
    print(f"   3. Saisir les données manuellement (si terminal interactif)")

    import sys
    if sys.stdin.isatty():
        # Terminal interactif, on peut demander la saisie
        print(f"\n⌨️  Saisie manuelle:")
        return Societe(
            siren=format_siren(siren),
            raison_sociale=input("Raison sociale: "),
            forme_juridique=input("Forme juridique: "),
            capital=input("Capital (ex: 5 000 €): "),
            adresse=input("Adresse (ville): ") + " (France)",
            ville_rcs=input("Ville RCS: "),
            representant_nom=input("Nom représentant: "),
            representant_fonction=input("Fonction représentant: ")
        )
    else:
        # Pas de terminal interactif, lever une erreur
        raise ValueError(f"Aucune source de données disponible pour le SIREN {siren}")


if __name__ == "__main__":
    # Test de l'API SIRENE avec un SIREN réel
    print("Test de l'API SIRENE (INSEE)\n")
    print("Ce test va appeler l'API SIRENE pour récupérer des données réelles.")
    print("Note: Une clé API gratuite est requise pour fonctionner.\n")

    # Test avec un SIREN qui n'est pas dans les données de test
    # Utilisons le SIREN de Google France par exemple: 443061841
    print("=" * 60)
    print("Test API SIRENE: Google France (SIREN 443061841)")
    print("=" * 60)

    test_siren = "443061841"
    print(f"🔍 Recherche dans l'API SIRENE (INSEE)...")

    societe = fetch_from_sirene_api(test_siren)

    if societe:
        print(f"\n✅ Données récupérées avec succès:")
        print(f"   SIREN: {societe.siren}")
        print(f"   Raison sociale: {societe.raison_sociale}")
        print(f"   Forme juridique: {societe.forme_juridique}")
        print(f"   Capital: {societe.capital}")
        print(f"   Adresse: {societe.adresse}")
        print(f"   Ville RCS: {societe.ville_rcs}")
        print(f"   Représentant: {societe.representant_nom} ({societe.representant_fonction})")
    else:
        print(f"\n❌ L'API n'a pas retourné de données.")
        print(f"\nPour obtenir une clé API gratuite:")
        print(f"   1. Aller sur https://portail-api.insee.fr/")
        print(f"   2. Créer un compte et une application")
        print(f"   3. Souscrire au plan 'Public' de l'API Sirene")
        print(f"   4. Ajouter la clé dans config/settings.yaml")

    print()
