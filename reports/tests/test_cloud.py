# import pytest
# import asyncio
# import os

# # Ensure Django settings are loaded BEFORE importing cloud_upload
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_project.settings")
# import django
# django.setup()

# from reports.utils import cloud_upload

# @pytest.mark.asyncio
# async def test_cloud_upload(monkeypatch):
#     called = False

#     async def fake_upload_to_supabase(file_bytes, cloud_file_name):
#         nonlocal called
#         called = True
#         return {"url": "https://fake-url.com/dummy.zip"}

#     #  monkeypatch the real function name
#     monkeypatch.setattr(cloud_upload, "upload_to_supabase", fake_upload_to_supabase)

#     # Now simulate calling it (same way your view will later)
#     dummy_bytes = b"fake data"
#     result = await fake_upload_to_supabase(dummy_bytes, "test.zip")

#     assert called
#     assert "url" in result
import pytest
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_project.settings")
django.setup()

from reports.utils import cloud_upload

@pytest.mark.asyncio
async def test_cloud_upload(monkeypatch):
    called = False

    async def fake_upload_to_supabase(file_bytes, cloud_file_name):
        nonlocal called
        called = True
        assert isinstance(file_bytes, bytes)
        return {"url": f"https://fake.supabase.io/{cloud_file_name}"}

    monkeypatch.setattr(cloud_upload, "upload_to_supabase", fake_upload_to_supabase)

    dummy_bytes = b"fake data"
    cloud_file_name = "test_upload.zip"
    result = await cloud_upload.upload_to_supabase(dummy_bytes, cloud_file_name)

    assert called
    assert "url" in result
    assert result["url"].startswith("https://fake.supabase.io/")
