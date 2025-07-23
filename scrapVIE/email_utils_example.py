import smtplib
from email.message import EmailMessage

# Configuration SMTP (à adapter selon ton fournisseur)
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 465
SMTP_USER = 'votre_email'
SMTP_PASS = 'VOTRE_MOT_DE_PASSE_ICI'  # Remplace par ton mot de passe d'application Yahoo
RECIPIENT = 'votre_email'
SUBJECT = 'Résumé des nouveaux jobs VIE (Airbus, Thalès, VIE Business)'

def send_email(body, subject=SUBJECT, recipient=RECIPIENT):
    """
    Envoie un email avec le résumé des nouveaux jobs.
    
    Args:
        body (str): Contenu du message
        subject (str): Sujet du mail (optionnel)
        recipient (str): Destinataire (optionnel)
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
    print(f"Email envoyé à {recipient}")

# Instructions pour Yahoo :
# 1. Va sur https://login.yahoo.com/account/security
# 2. Clique sur "Gérer les mots de passe d'application"
# 3. Choisis "Autre application" (ex: "Python")
# 4. Copie le mot de passe généré et remplace VOTRE_MOT_DE_PASSE_ICI 