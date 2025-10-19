# reports/tests/test_full_system.py
import os
import django
import pytest
from django.core import mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_project.settings")
django.setup()

from reports.utils import cloud_upload, email_notification


@pytest.mark.django_db
def test_full_system_integration(monkeypatch, settings):
    """
     Full integration test that simulates:
    1. Generating report data
    2. Uploading to Supabase (mocked)
    3. Sending email notification to admin
    """

    # Configure test-safe email backend
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.EMAIL_HOST_USER = "admin@example.com"
    settings.DEFAULT_FROM_EMAIL = "noreply@example.com"

    # Mock cloud upload (pretend success)
    called = {"upload": False}

    def fake_upload_to_supabase(file_bytes, cloud_file_name):
        called["upload"] = True
        assert isinstance(file_bytes, (bytes, bytearray))
        return f"https://supabase.fake/{cloud_file_name}"

    monkeypatch.setattr(cloud_upload, "upload_to_supabase", fake_upload_to_supabase)

    # 1️ Simulate upload
    fake_file = b"sample data"
    url = cloud_upload.upload_to_supabase(fake_file, "student_reports.zip")

    assert called["upload"], "Upload was not triggered"
    assert url.startswith("https://supabase.fake/")

    # 2️ Send email with link
    email_notification.notify_admin("Reports Ready", f"Your reports are available here: {url}")

    # 3️ Verify email sent successfully
    assert len(mail.outbox) == 1, "Email was not sent"
    email = mail.outbox[0]
    assert "Reports Ready" in email.subject
    assert url in email.body
    assert "admin@example.com" in email.to
