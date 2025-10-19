from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ============================================================
# Profile (Unified model for all users)
# ============================================================
class Profile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("lecturer", "Lecturer"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    # Student-specific fields
    registration_number = models.CharField(max_length=100, blank=True, null=True, unique=False)

    # Lecturer-specific fields
    department = models.CharField(max_length=100, blank=True, null=True)
    office_number = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


# ============================================================
# Academic Models
# ============================================================
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credit_units = models.IntegerField(default=3)
    lecturer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'lecturer'},
        related_name="taught_courses"
    )
    students = models.ManyToManyField(
        Profile,
        limit_choices_to={'role': 'student'},
        related_name="enrolled_courses",
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class StudentMark(models.Model):
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name="marks"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'lecturer'},
        related_name="given_marks"
    )
    score = models.FloatField()
    grade = models.CharField(max_length=2, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    cpa = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f"{self.student.name} - {self.course.name} ({self.score})"


# ============================================================
# Clubs & Student Life
# ============================================================
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    meeting_time = models.CharField(max_length=50, blank=True)
    members = models.ManyToManyField(Profile, related_name="clubs", blank=True)

    def __str__(self):
        return self.name


class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"


# ============================================================
# Careers & Internships
# ============================================================
class CareerOpportunity(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    deadline = models.DateField()
    link = models.URLField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.company} - {self.role}"


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.student.name} on {self.course.name}"


class SavedOpportunity(models.Model):
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    opportunity = models.ForeignKey(CareerOpportunity, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# Achievements & Endorsements
# ============================================================
class Achievement(models.Model):
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.title}"


class Endorsement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    endorsed_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# Support & Services
# ============================================================
class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]

    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class TicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    responder = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
