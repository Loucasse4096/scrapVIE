# scrapVIE

Ce projet est un scraper Python pour récupérer les offres VIE depuis Airbus, Thalès et VIE Business, avec envoi automatique par email des nouveaux jobs trouvés.

## Structure du projet
- `main.py` : Point d'entrée principal du projet avec scraping et envoi d'email.
- `email_utils.py` : Configuration et fonctions d'envoi d'email (à créer avec tes identifiants).
- `requirements.txt` : Dépendances Python.

## Installation

### Sur ta machine locale
```bash
# Cloner le repository
git clone https://github.com/Loucasse4096/scrapVIE.git
cd scrapVIE

# Installer les dépendances
pip install -r requirements.txt

# Créer email_utils.py avec tes identifiants
cp email_utils_example.py email_utils.py
# Éditer email_utils.py et remplacer VOTRE_MOT_DE_PASSE_ICI

# Tester
python main.py --all
```

### Sur Raspberry Pi
```bash
# Se connecter au Pi
ssh lambda@192.168.1.203

# Cloner le repository
cd /home/lambda
git clone https://github.com/Loucasse4096/scrapVIE.git
cd scrapVIE

# Installer les dépendances
pip3 install -r requirements.txt

# Créer email_utils.py avec tes identifiants
nano email_utils.py
# Copier le contenu et remplacer VOTRE_MOT_DE_PASSE_ICI

# Tester
python3 main.py --all
```

## Utilisation

### Scraping manuel
```bash
# Tous les sites
python main.py --all

# Un site spécifique
python main.py --site airbus
python main.py --site thales
python main.py --site vie_business

# Mode debug
python main.py --all --debug
```

### Exécution automatique sur Raspberry Pi

#### Option 1 : Avec cron (recommandé)
```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour exécuter toutes les heures
0 * * * * cd /home/lambda/scrapVIE && /usr/bin/python3 main.py --all >> /home/lambda/scrapVIE/scraping.log 2>&1

# Vérifier que cron est actif
sudo systemctl status cron
sudo systemctl enable cron
```

#### Option 2 : Avec systemd (plus robuste)
```bash
# Créer le service systemd
sudo nano /etc/systemd/system/scrapvie.service
```

Contenu du service :
```ini
[Unit]
Description=ScrapVIE Job Scraper
After=network.target

[Service]
Type=oneshot
User=lambda
WorkingDirectory=/home/lambda/scrapVIE
ExecStart=/usr/bin/python3 main.py --all
StandardOutput=append:/home/lambda/scrapVIE/scraping.log
StandardError=append:/home/lambda/scrapVIE/scraping.log

[Install]
WantedBy=multi-user.target
```

```bash
# Créer le timer
sudo nano /etc/systemd/system/scrapvie.timer
```

Contenu du timer :
```ini
[Unit]
Description=Run ScrapVIE every hour
Requires=scrapvie.service

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# Activer et démarrer
sudo systemctl daemon-reload
sudo systemctl enable scrapvie.timer
sudo systemctl start scrapvie.timer

# Vérifier le statut
sudo systemctl status scrapvie.timer
sudo systemctl list-timers
```

#### Vérification et logs
```bash
# Voir les logs
tail -f /home/lambda/scrapVIE/scraping.log

# Vérifier les fichiers JSON générés
ls -la /home/lambda/scrapVIE/*_jobs.json

# Vérifier le statut du service/timer
sudo systemctl status scrapvie.timer
crontab -l
```

## Configuration

### Email
Éditer `email_utils.py` avec tes identifiants Yahoo :
- `SMTP_PASS` : Ton mot de passe d'application Yahoo (pas le mot de passe principal)
- `RECIPIENT` : Adresse email de destination

### Fichiers de sortie
- `airbus_jobs.json` : Offres Airbus
- `thales_jobs.json` : Offres Thalès  
- `vie_business_jobs.json` : Offres VIE Business

## Déploiement
Le projet est conçu pour être déployé sur Raspberry Pi avec exécution automatique via cron ou systemd.

## Mise à jour
```bash
# Sur le Pi
cd /home/lambda/scrapVIE
git pull
``` 