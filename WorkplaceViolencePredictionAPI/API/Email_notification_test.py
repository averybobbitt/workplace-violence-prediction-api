import logging
import os

from django.core.mail import send_mail, get_connection

from WorkplaceViolencePredictionAPI import settings


settings.DEBUG = True
settings.ALLOWED_HOSTS = ['localhost', 'smtp.gmail.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "wpvprediction@gmail.com"
EMAIL_HOST_PASSWORD = "gujwjdvulejbeygg"


def execute():
    bcc_recipients = []

    # Now the emails are pulled from a separate text file that can be altered as needed
    with open('emails.txt', 'r') as file:
        for line in file:
            recipient = line.strip()
            bcc_recipients.append(recipient)

    print(bcc_recipients)

    connection = get_connection(
        backend=EMAIL_BACKEND,
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS
    )

    # Department and risk can be filled in with more specific information later.
    # This is only a test to make sure the message works.
    message = (
        "Warning: Risk levels in the hospital!",
        "This message is to inform you of high risk levels within the hospital. "
        "Please be cautious of heightened stress levels as we work to resolve the issue.",
        EMAIL_HOST_USER,
        bcc_recipients,
    )

    # Simple test of email sending function. Later on, I will setup a mass_email
    # function that we can feed all of our gathered emails into (probably at once)
    try:
        send_mail(*message, connection=connection, fail_silently=False)
    except Exception as e:
        logging.error(f"Error sending email: {e}")
