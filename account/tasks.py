from celery import shared_task
from django.core.mail import EmailMessage
from smtplib import SMTPException, SMTPAuthenticationError


@shared_task(name="send welcome email task")
def send_welcome_email_task(subject, message, from_email, to):

    mail = EmailMessage(subject, message, from_email, to)
    try:
        mail.send(fail_silently=False)
    except SMTPAuthenticationError or SMTPException:
        return f"FAILED TO SEND EMAIL TO {to}"
    return "SUCCESS"
