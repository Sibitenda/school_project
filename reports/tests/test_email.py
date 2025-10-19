# reports/tests/test_email.py
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_project.settings")
django.setup()

import pytest
from django.core import mail
from reports.utils.email_notification import notify_admin

@pytest.mark.django_db
def test_email_notification(settings):
    """
    Tests that notify_admin sends an email correctly
    and stores it in the local memory backend.
    """
    settings.EMAIL_HOST_USER = "test@example.com"
    settings.DEFAULT_FROM_EMAIL = "noreply@example.com"
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    notify_admin("Test Subject", "This is a test message.")

    assert len(mail.outbox) == 1, "Expected one email to be sent"
    sent_email = mail.outbox[0]
    assert sent_email.subject == "Test Subject"
    assert "This is a test message." in sent_email.body
    assert sent_email.to == ["test@example.com"]
