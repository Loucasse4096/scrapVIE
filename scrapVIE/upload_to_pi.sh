#!/bin/bash

# Script pour uploader le projet sur le Raspberry Pi
# Usage : ./upload_to_pi.sh

PI_USER="lambda"
PI_HOST="192.168.1.203"
PI_PASS="accp47un"
PI_PATH="/home/lambda/scrapVIE"

# Installer sshpass si non présent
if ! command -v sshpass &> /dev/null
then
    echo "sshpass n'est pas installé. Veuillez l'installer (ex: brew install hudochenkov/sshpass/sshpass ou sudo apt install sshpass)"
    exit 1
fi

# Créer le dossier sur le Pi si besoin
sshpass -p "$PI_PASS" ssh -o StrictHostKeyChecking=no $PI_USER@$PI_HOST "mkdir -p $PI_PATH"

# Uploader le dossier
sshpass -p "$PI_PASS" rsync -avz --delete --exclude='__pycache__' ./ $PI_USER@$PI_HOST:$PI_PATH

echo "Upload terminé !" 