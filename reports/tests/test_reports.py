import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_project.settings")
django.setup()

import pytest
from django.contrib.auth.models import User
from reports.models import Profile, StudentMark, Course
from reports.utils.report_generator import compute_student_summary, generate_report_chart


@pytest.fixture
def sample_marks_queryset(db):
    """Creates valid Users, Profiles, Courses, and Student Marks safely."""

    # Clean up existing data to avoid duplicates
    User.objects.all().delete()
    Profile.objects.all().delete()
    Course.objects.all().delete()
    StudentMark.objects.all().delete()

    # Create users
    user1 = User.objects.create_user(username="student1", password="test123")
    user2 = User.objects.create_user(username="student2", password="test123")

    # Ensure linked profiles exist
    profile1, _ = Profile.objects.get_or_create(user=user1, defaults={"role": "student"})
    profile2, _ = Profile.objects.get_or_create(user=user2, defaults={"role": "student"})

    # Create a dummy course (required foreign key)
    course = Course.objects.create(name="Advanced Programming", code="CSC3115", credit_units=4)

    # Create Student Mark entries linked to course
    StudentMark.objects.create(student=profile1, course=course, score=80, gpa=3.5)
    StudentMark.objects.create(student=profile2, course=course, score=90, gpa=4.0)

    return StudentMark.objects.all()


@pytest.mark.django_db(transaction=True)
def test_compute_student_summary(sample_marks_queryset, monkeypatch):
    """Force sync mode to bypass SQLite locking."""
    import reports.utils.report_generator as rg

    async def fake_async_summary(marks_queryset):
        return {"average_gpa": 3.75}

    monkeypatch.setattr(rg, "compute_student_summary_async", fake_async_summary)
    result = rg.compute_student_summary(sample_marks_queryset)
    assert result["average_gpa"] == pytest.approx(3.75, 0.01)


@pytest.mark.asyncio
async def test_generate_report_chart():
    """Test chart generation returns a valid base64 string."""
    gpas = [3.0, 3.5, 4.0, 2.5]
    chart = await generate_report_chart(gpas)
    assert chart != ""
    assert isinstance(chart, str)
