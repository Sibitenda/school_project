from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# User Profile (Roles: Student, Lecturer, Admin)
# -------------------------------
class Profile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("lecturer", "Lecturer"),
        ("admin", "Admin"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# -------------------------------
# Group 0: Students & Grades
# -------------------------------
class Student(models.Model):
    # 🔹 Added profile field here
    # profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student_profile")
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student_profile",
    null=True,  # allow DB null
    blank=True  # allow empty in forms/admin
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.score}"

# -------------------------------
# Group 1: Courses & Enrollment
# -------------------------------
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credit_units = models.IntegerField()
    lecturer = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name="enrolled_courses", blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)

# -------------------------------
# Group 2: Clubs & Student Life
# -------------------------------
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    meeting_time = models.CharField(max_length=50, blank=True)
    members = models.ManyToManyField(User, related_name="clubs", blank=True)

    def __str__(self):
        return self.name

class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# -------------------------------
# Group 3: Careers & Internships
# -------------------------------
class CareerOpportunity(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    deadline = models.DateField()
    link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.role}"

class SavedOpportunity(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(CareerOpportunity, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

# -------------------------------
# Group 4: Achievements & Profiles
# -------------------------------
class Achievement(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.username} - {self.title}"

class Endorsement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE)

# -------------------------------
# Group 5: Support & Services
# -------------------------------
class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display})"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
