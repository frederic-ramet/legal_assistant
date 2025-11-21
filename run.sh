#!/bin/bash

# Script interactif pour le générateur de contrats
# Usage: ./run.sh

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
print_header() {
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Vérifier les dépendances
check_dependencies() {
    print_header "VÉRIFICATION DES DÉPENDANCES"

    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 n'est pas installé"
        exit 1
    fi
    print_success "Python 3 installé: $(python3 --version)"

    # Vérifier pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 n'est pas installé"
        exit 1
    fi
    print_success "pip3 installé"

    # Vérifier si les dépendances sont installées
    echo ""
    print_info "Vérification des packages Python..."

    if python3 -c "import requests, docx, yaml" 2>/dev/null; then
        print_success "Tous les packages Python sont installés"
    else
        print_warning "Certains packages manquent"
        echo ""
        read -p "Voulez-vous installer les dépendances maintenant ? (o/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Oo]$ ]]; then
            print_info "Installation des dépendances..."
            pip3 install -r requirements.txt
            if [ $? -eq 0 ]; then
                print_success "Dépendances installées avec succès"
            else
                print_error "Erreur lors de l'installation des dépendances"
                exit 1
            fi
        else
            print_error "Installation annulée. Exécutez: pip3 install -r requirements.txt"
            exit 1
        fi
    fi

    echo ""
}

# Menu principal
show_main_menu() {
    clear
    print_header "GÉNÉRATEUR DE CONTRATS JURIDIQUES"
    echo ""
    echo "Que souhaitez-vous faire ?"
    echo ""
    echo "  1) Générer un NDA (Accord de confidentialité)"
    echo "  2) Afficher l'aide"
    echo "  3) Tester l'API SIRENE (requiert clé API)"
    echo "  4) Quitter"
    echo ""
    read -p "Votre choix (1-4): " choice

    case $choice in
        1) generate_nda ;;
        2) show_help ;;
        3) test_scraper ;;
        4) exit 0 ;;
        *)
            print_error "Choix invalide"
            sleep 2
            show_main_menu
            ;;
    esac
}

# Générer un NDA
generate_nda() {
    clear
    print_header "GÉNÉRATION D'UN NDA"

    # Choix de la variante
    echo ""
    echo "Choisissez le type de NDA :"
    echo ""
    echo "  1) master          - Conseil IA générique (sans clause non-sollicitation)"
    echo "  2) dev_plateforme  - Développement plateforme ForgeAI (avec non-sollicitation 12 mois)"
    echo "  3) prestations     - Missions clients FR Digital (avec non-sollicitation 12 mois)"
    echo ""
    read -p "Votre choix (1-3): " variant_choice

    case $variant_choice in
        1) variant="master" ;;
        2) variant="dev_plateforme" ;;
        3) variant="prestations" ;;
        *)
            print_error "Choix invalide"
            sleep 2
            generate_nda
            return
            ;;
    esac

    print_info "Variante sélectionnée: $variant"
    echo ""

    # Demander l'identifiant de la société partenaire (Partie 2)
    echo "Entrez l'identifiant de la société partenaire (Partie 2) :"
    echo ""
    echo "  Exemples :"
    echo "    - URL Pappers : https://www.pappers.fr/entreprise/nexans-393525852"
    echo "    - SIREN       : 393525852"
    echo ""
    echo "  Sociétés de test disponibles :"
    echo "    - FR Digital  : 901995308"
    echo "    - Nexans      : 393525852"
    echo ""
    read -p "Identifiant : " party_id

    if [ -z "$party_id" ]; then
        print_error "Identifiant vide"
        sleep 2
        generate_nda
        return
    fi

    # Répertoire de sortie
    output_dir="output"

    # Générer le NDA
    echo ""
    print_info "Génération en cours..."
    echo ""

    python3 -m src.cli nda --party "$party_id" --type "$variant" --output "$output_dir"

    exit_code=$?

    echo ""
    if [ $exit_code -eq 0 ]; then
        print_success "NDA généré avec succès dans le dossier $output_dir/"
        echo ""
        echo "Fichiers générés :"
        ls -lh $output_dir/*.docx 2>/dev/null | tail -1
    else
        print_error "Erreur lors de la génération"
    fi

    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
    show_main_menu
}

# Afficher l'aide
show_help() {
    clear
    print_header "AIDE - UTILISATION DU GÉNÉRATEUR"

    echo ""
    echo "USAGE EN LIGNE DE COMMANDE :"
    echo ""
    echo "  python3 -m src.cli nda --party <identifiant> --type <variante>"
    echo ""
    echo "OPTIONS :"
    echo ""
    echo "  --party <identifiant>   URL Pappers ou SIREN de la société partenaire"
    echo "  --type <variante>       Type de NDA : master, dev_plateforme, prestations"
    echo "  --output <dossier>      Répertoire de sortie (défaut: output/)"
    echo ""
    echo "EXEMPLES :"
    echo ""
    echo "  # NDA master avec SIREN"
    echo "  python3 -m src.cli nda --party \"393525852\" --type master"
    echo ""
    echo "  # NDA dev plateforme avec URL"
    echo "  python3 -m src.cli nda \\"
    echo "    --party \"https://www.pappers.fr/entreprise/nexans-393525852\" \\"
    echo "    --type dev_plateforme"
    echo ""
    echo "VARIANTES NDA :"
    echo ""
    echo "  master          : Conseil IA générique"
    echo "  dev_plateforme  : Développement plateforme ForgeAI"
    echo "  prestations     : Missions clients FR Digital"
    echo ""
    echo "SOCIÉTÉS DE TEST :"
    echo ""
    echo "  FR Digital : 901995308"
    echo "  Nexans     : 393525852"
    echo ""

    read -p "Appuyez sur Entrée pour revenir au menu..."
    show_main_menu
}

# Tester le scraper
test_scraper() {
    clear
    print_header "TEST DE L'API SIRENE"

    echo ""
    print_info "Test de l'API SIRENE avec un SIREN réel (Google France)..."
    print_warning "Note: Requiert une clé API gratuite de https://portail-api.insee.fr/"
    echo ""

    python3 -m src.scraper

    echo ""
    read -p "Appuyez sur Entrée pour revenir au menu..."
    show_main_menu
}

# Script principal
main() {
    check_dependencies
    show_main_menu
}

# Lancer le script
main
