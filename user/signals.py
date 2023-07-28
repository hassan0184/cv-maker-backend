from .models import *
import threading

from cvmaker.settings import * 

from django.core.mail import EmailMessage, get_connection
from django.dispatch import receiver
from django.db.models.signals import post_save


def send_welcome_email(subject, message, email_from, recipient_list):
    with get_connection(
            host=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD,
            use_tls=EMAIL_USE_TLS
    ) as connection:
        email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
        email.send()

@receiver(post_save, sender=User)
def send_mail_to_repoter(sender, instance, created, **kwargs):
    if created:
        
        subject = 'Welcome to Family'
        email_from = EMAIL_HOST_USER
        recipient_list = [instance.email]
        message = f'''
            Dear {instance.first_name},

            Welcome to the CV-MAKER family! We are thrilled to have you on board.

            Your journey with us begins today, and we are here to support you every step of the way as you create your remarkable CV.

            At CV-MAKER, we believe in empowering individuals like you to showcase your talents, skills, and accomplishments through beautifully crafted resumes.

            If you ever need assistance, have questions, or want to share your success stories, our team is just an email away. We're more than happy to help.

            Thank you for choosing CV-MAKER. We can't wait to see the amazing CV you'll create!

            Best regards,
            The CV-MAKER Team
        '''

        # Create a new thread to send the email in the background
        email_thread = threading.Thread(
            target=send_welcome_email,
            args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()