from django.conf.global_settings import EMAIL_BACKEND
from django.core.mail import send_mail
import logging
import os
from django.conf import settings

#ungant67@students.rowan.edu
#dipiet77@students.rowan.edu
#duymch27@students.rowan.edu
#bobbit82@rowan.edu
#profic93@students.rowan.edu

bcc_recipients = []

#Now the emails are pulled from a separate text file that can be altered as needed
with open('workplace-violence-prediction-api/emails.txt', 'r') as file:
    for line in file:
        recipient = line.strip()
        bcc_recipients.append(recipient)

#print(recipients)

# Manually configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '')
settings.configure(
    DEBUG=True,
    ALLOWED_HOSTS=['localhost', 'smtp.gmail.com'],
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER="wpvprediction@gmail.com",
    EMAIL_HOST_PASSWORD="gujwjdvulejbeygg"
)

#Department and risk can be filled in with more specific information later.
#This is only a test to make sure the message works.

message = (
    "Warning: Risk levels in the hospital!",
    "This message is to inform you of high risk levels within the hospital. "
    "Please be cautious of heightened stress levels as we work to resolve the issue.",
    "workplaceviolencePrediction@gmail.com",
    ["workplaceviolencePrediction@gmail.com"],
)

#Simple test of email sending function. Later on, I will setup a mass_email
#function that we can feed all of our gathered emails into (probably at once)
try:
    send_mail(*message, fail_silently=False)
except Exception as e:
    logging.error(f"Error sending email: {e}")
