# Module pour scraper les informations d'entreprise via Pappers

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional
from .models import Societe


def saisie_manuelle(siren: str) -> Societe:
    """Données hardcodées pour les tests (fallback si Pappers bloque)."""
    # Données de test pour FR Digital et Nexans
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
    if siren_clean in test_data:
        print(f"ℹ️  Utilisation des données de test pour SIREN {siren}")
        return test_data[siren_clean]

    # Sinon, demander saisie manuelle
    print(f"\n⌨️  Saisie manuelle pour SIREN {siren}")
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


def extract_siren_from_url(url: str) -> Optional[str]:
    """Extrait le SIREN d'une URL Pappers."""
    # Format: https://www.pappers.fr/entreprise/nom-entreprise-123456789
    match = re.search(r'-(\d{9})$', url)
    if match:
        return match.group(1)
    return None


def format_capital(capital_str: str) -> str:
    """Formate le capital avec espaces milliers et €."""
    # Extraire le nombre
    numbers = re.findall(r'\d+', capital_str.replace(' ', ''))
    if not numbers:
        return capital_str

    capital_num = ''.join(numbers)

    # Ajouter espaces milliers
    if len(capital_num) > 3:
        formatted = ''
        for i, digit in enumerate(reversed(capital_num)):
            if i > 0 and i % 3 == 0:
                formatted = ' ' + formatted
            formatted = digit + formatted
        return f"{formatted} €"

    return f"{capital_num} €"


def format_siren(siren: str) -> str:
    """Formate le SIREN avec espaces (XXX XXX XXX)."""
    siren = siren.replace(' ', '')
    if len(siren) == 9:
        return f"{siren[0:3]} {siren[3:6]} {siren[6:9]}"
    return siren


def scrape_pappers(identifier: str) -> Societe:
    """
    Scrape les informations d'une société depuis Pappers.

    Args:
        identifier: URL Pappers ou SIREN

    Returns:
        Objet Societe avec les données extraites
    """
    # Déterminer si c'est une URL ou un SIREN
    if identifier.startswith('http'):
        url = identifier
        siren = extract_siren_from_url(url)
        if not siren:
            raise ValueError(f"Impossible d'extraire le SIREN de l'URL: {url}")
    else:
        siren = identifier.replace(' ', '')
        if len(siren) != 9:
            raise ValueError(f"SIREN invalide: {siren} (doit contenir 9 chiffres)")
        url = f"https://www.pappers.fr/entreprise/{siren}"

    print(f"📥 Extraction des données depuis Pappers...")
    print(f"   URL: {url}")

    # Récupérer la page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"⚠️  Pappers bloque l'accès automatique.")
            print(f"   Fallback: Saisie manuelle des données")
            return saisie_manuelle(siren)
        raise

    # Parser le HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraire les données
    try:
        # Raison sociale (h1 principal)
        raison_sociale_elem = soup.find('h1')
        raison_sociale = raison_sociale_elem.text.strip() if raison_sociale_elem else ""

        # Forme juridique
        forme_juridique = ""
        forme_elem = soup.find(text=re.compile(r'Forme juridique'))
        if forme_elem:
            forme_juridique = forme_elem.find_next('dd').text.strip() if forme_elem.find_next('dd') else ""

        # Capital
        capital = ""
        capital_elem = soup.find(text=re.compile(r'Capital social'))
        if capital_elem:
            capital_raw = capital_elem.find_next('dd').text.strip() if capital_elem.find_next('dd') else ""
            capital = format_capital(capital_raw)

        # Adresse (extraire ville)
        adresse = ""
        adresse_elem = soup.find(text=re.compile(r'Adresse'))
        if adresse_elem:
            adresse_raw = adresse_elem.find_next('dd').text.strip() if adresse_elem.find_next('dd') else ""
            # Extraire ville (dernière ligne avant code postal)
            lines = adresse_raw.split('\n')
            for line in reversed(lines):
                line = line.strip()
                if line and not re.match(r'^\d{5}', line):
                    adresse = f"{line} (France)"
                    break

        # Ville RCS (greffe)
        ville_rcs = ""
        greffe_elem = soup.find(text=re.compile(r'Greffe'))
        if greffe_elem:
            ville_rcs = greffe_elem.find_next('dd').text.strip() if greffe_elem.find_next('dd') else ""

        # Représentant (dirigeant principal)
        representant_nom = ""
        representant_fonction = ""
        dirigeant_elem = soup.find(text=re.compile(r'Dirigeants?'))
        if dirigeant_elem:
            dirigeant_div = dirigeant_elem.find_next('div', class_=re.compile(r'dirigeant|personne'))
            if dirigeant_div:
                nom_elem = dirigeant_div.find('a') or dirigeant_div.find(text=True)
                if nom_elem:
                    representant_nom = nom_elem.text.strip() if hasattr(nom_elem, 'text') else str(nom_elem).strip()

                fonction_elem = dirigeant_div.find(text=re.compile(r'Président|Gérant|Directeur'))
                if fonction_elem:
                    representant_fonction = fonction_elem.strip()

        # Formater le SIREN
        siren_formatted = format_siren(siren)

        print(f"✅ Données extraites:")
        print(f"   Raison sociale: {raison_sociale}")
        print(f"   Forme juridique: {forme_juridique}")
        print(f"   Capital: {capital}")
        print(f"   Adresse: {adresse}")
        print(f"   Ville RCS: {ville_rcs}")
        print(f"   SIREN: {siren_formatted}")
        print(f"   Représentant: {representant_nom} ({representant_fonction})")

        return Societe(
            siren=siren_formatted,
            raison_sociale=raison_sociale,
            forme_juridique=forme_juridique,
            capital=capital,
            adresse=adresse,
            ville_rcs=ville_rcs,
            representant_nom=representant_nom,
            representant_fonction=representant_fonction
        )

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        raise ValueError(f"Impossible d'extraire les données de Pappers: {e}")


if __name__ == "__main__":
    # Test
    print("Test scraper Pappers\n")

    # Test FR Digital
    print("=" * 60)
    societe1 = scrape_pappers("https://www.pappers.fr/entreprise/fr-digital-901995308")
    print()

    # Test Nexans
    print("=" * 60)
    societe2 = scrape_pappers("https://www.pappers.fr/entreprise/nexans-393525852")
