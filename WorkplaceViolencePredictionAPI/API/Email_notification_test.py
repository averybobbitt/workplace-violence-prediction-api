import logging
import os
from email.message import EmailMessage
from WorkplaceViolencePredictionAPI import settings
from django.core.mail import get_connection, EmailMessage

from dotenv import load_dotenv

load_dotenv(dotenv_path='email.env')

# This info should be stored somewhere else and pulled into here. I have it here now for testing purposes
settings.DEBUG = True
settings.ALLOWED_HOSTS = ['localhost', 'smtp.gmail.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = str(os.environ.get('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.environ.get('EMAIL_HOST_PASSWORD'))

bcc_recipients = []


def append(email):
    if isinstance(email, str):
        f = open('emails.txt', 'a+')
        f.write("\n"+email)
        f.close()
        with open('emails.txt', 'r+') as f:
            n = f.readlines()
            f.seek(0)
            for line in n:
                if line.strip() != '':
                    f.write(line)
            f.truncate()
    else:
        print("ERROR: WRONG INPUT TYPE")


def remove(email):
    if isinstance(email, str):
        with open('emails.txt', 'r+') as f:
            n = f.readlines()
            f.seek(0)
            for line in n:
                if line.strip() != email:
                    f.write(line)
            f.truncate()

    else:
        print("ERROR: WRONG INPUT TYPE")


def execute():
    # The emails are pulled from a separate text file that can be altered as needed
    with open('emails.txt', 'r') as file:
        for line in file:
            recipient = line.strip()
            bcc_recipients.append(recipient)

    connection = get_connection(
        backend=EMAIL_BACKEND,
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=True
    )

    # Email sends message to itself and BCCs a list of recipients
    try:
        email = EmailMessage(
            subject="Warning: Risk levels in the hospital!",
            body="This message is to inform you of high risk levels within the hospital. "
                 "Please be cautious of heightened stress levels as we work to resolve the issue.",
            bcc=bcc_recipients,
            from_email=EMAIL_HOST_USER,
            to=[EMAIL_HOST_USER],
            connection=connection,
        )

        email.send()
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def list():
    with open("emails.txt", "r") as file:
        return file.read()