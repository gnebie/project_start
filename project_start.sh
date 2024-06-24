#!/bin/bash

# Usage
# ./start.sh -p /chemin/vers/projet
# export PROJECT_PATH_ENV=/chemin/vers/projet
# ./start.sh

set -e 
# Fonction d'affichage de l'aide
function show_help {
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -p, --path      Absolute path to the project directory"
    echo "  -h, --help      Show this help message and exit"
    echo
    echo "Environment Variables:"
    echo "  PROJECT_PATH    Absolute path to the project directory"
}

# Variables par défaut
PROJECT_PATH=""
VENV_PATH="/home/gnebie/sandbox/stablediffusion/sdweb_client/tools/project_start/venv"
TEMPLATE_PATH="/home/gnebie/sandbox/stablediffusion/sdweb_client/tools/project_start/project_start_files"

# Analyse des arguments de la ligne de commande
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--path) PROJECT_PATH="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Fonction pour copier les fichiers sans écraser
function copy_if_not_exists {
    local src=$1
    local dest=$2
    if [ -e "$dest" ]; then
        echo "File $dest already exists. Skipping."
    else
        cp -r "$src" "$dest"
        echo "Copied $src to $dest."
    fi
}

# Si PROJECT_PATH n'est pas défini, vérifier la variable d'environnement
if [ -z "$PROJECT_PATH" ]; then
    PROJECT_PATH=${PROJECT_PATH_ENV:-}
fi

# Si PROJECT_PATH n'est toujours pas défini, demander à l'utilisateur
if [ -z "$PROJECT_PATH" ]; then
    read -p "Please enter the absolute path to the project directory: " PROJECT_PATH
fi

# Vérification finale
if [ -z "$PROJECT_PATH" ]; then
    echo "Error: Project path is required."
    show_help
    exit 1
fi

# Affichage des valeurs pour vérification
echo "Project Path: $PROJECT_PATH"

# Création du répertoire de projet
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

source $VENV_PATH/bin/activate

# Exécution de cookiecutter pour le template
cookiecutter $TEMPLATE_PATH

deactivate

# Copie du répertoire virtuel
# cp -r $VENV_PATH .
# python -m venv venv

echo "Project setup complete at $PROJECT_PATH"
