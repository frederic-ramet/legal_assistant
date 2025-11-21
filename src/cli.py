# Interface en ligne de commande pour le générateur de contrats

import argparse
import sys
from pathlib import Path

# Ajouter le répertoire parent au PATH pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import scrape_pappers
from src.generator import generate_nda


def main():
    """Point d'entrée principal du CLI."""
    parser = argparse.ArgumentParser(
        description="Générateur de contrats juridiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Générer un NDA master entre deux sociétés
  python -m src.cli nda \\
    --party "https://www.pappers.fr/entreprise/fr-digital-901995308" \\
    --party "https://www.pappers.fr/entreprise/nexans-393525852" \\
    --type master

  # Avec SIREN direct
  python -m src.cli nda --party "901995308" --party "393525852" --type master

  # NDA dev plateforme
  python -m src.cli nda --party "393525852" --type dev_plateforme
        """
    )

    # Sous-commandes par type de contrat
    subparsers = parser.add_subparsers(dest='contract_type', help='Type de contrat')

    # Commande NDA
    nda_parser = subparsers.add_parser('nda', help='Générer un accord de confidentialité')
    nda_parser.add_argument(
        '--party',
        action='append',
        required=True,
        help='URL Pappers ou SIREN de la société partenaire (Partie 2). Peut être spécifié plusieurs fois.'
    )
    nda_parser.add_argument(
        '--type',
        default='master',
        choices=['master', 'dev_plateforme', 'prestations'],
        help='Type de NDA (défaut: master)'
    )
    nda_parser.add_argument(
        '--output',
        default='output',
        help='Répertoire de sortie (défaut: output/)'
    )

    args = parser.parse_args()

    if not args.contract_type:
        parser.print_help()
        sys.exit(1)

    # Traitement selon le type de contrat
    if args.contract_type == 'nda':
        handle_nda(args)
    else:
        print(f"❌ Type de contrat non supporté: {args.contract_type}")
        sys.exit(1)


def handle_nda(args):
    """Traite la génération d'un NDA."""
    print("=" * 70)
    print("📋 GÉNÉRATEUR NDA")
    print("=" * 70)

    parties = []

    # Note: Pour le NDA, on ne prend que la première partie (partie 2)
    # FR Digital (partie 1) est hardcodé dans le template
    if len(args.party) > 1:
        print("ℹ️  Note: NDA bilatéral. Seule la première société sera utilisée comme Partie 2.")
        print("   FR Digital est automatiquement Partie 1.\n")

    party_identifier = args.party[0]

    print(f"\n📥 Extraction des données de la Partie 2...")
    print(f"   Identifiant: {party_identifier}\n")

    try:
        # Scraper la société
        partie2 = scrape_pappers(party_identifier)
        print()

        # Générer le NDA
        output_file = generate_nda(
            partie2=partie2,
            variant=args.type,
            output_dir=args.output
        )

        print("\n" + "=" * 70)
        print("✅ GÉNÉRATION TERMINÉE")
        print("=" * 70)
        print(f"📄 Fichier: {output_file}")
        print(f"🎯 Type: NDA {args.type}")
        print(f"👥 Parties:")
        print(f"   - FR DIGITAL (Partie 1)")
        print(f"   - {partie2.raison_sociale} (Partie 2)")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
