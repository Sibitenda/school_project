# reports/utils/email_notification.py
from django.core.mail import send_mail
from django.conf import settings

def notify_admin(subject, message, recipient_list=None):
    """
    Sends an email notification to admin or specific recipients.
    Defaults to the EMAIL_HOST_USER if none is provided.
    """
    if recipient_list is None:
        recipient_list = [getattr(settings, "EMAIL_HOST_USER", "admin@example.com")]

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        recipient_list=recipient_list,
        fail_silently=False,
    )
