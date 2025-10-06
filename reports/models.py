
from django.db import models
from django.contrib.auth.models import User
from reports.utils.grade_utils import calculate_grade_and_gpa
# or using helper exposed in __init__
from reports.utils import calculate_grade_and_gpa, compute_student_summary

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# from .models import StudentMark



# ============================================================
# Group 0: User Profiles & Roles
# # ============================================================
# class Profile(models.Model):
#     ROLE_CHOICES = [
#         ("student", "Student"),
#         ("lecturer", "Lecturer"),
#         ("admin", "Admin"),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

#     def __str__(self):
#         return f"{self.user.username} ({self.role})"

class Profile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("lecturer", "Lecturer"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True)  # ✅ add this line

    def __str__(self):
        return self.name or self.user.username
# @receiver(post_save, sender=Profile)
# def create_related_profile(sender, instance, created, **kwargs):
#     """
#     Automatically create LecturerProfile or StudentProfile
#     when a new Profile is created.
#     """
#     if created:
#         # Import inside to avoid circular import errors
#         from .models import LecturerProfile, StudentProfile

#         if instance.role == 'lecturer':
#             LecturerProfile.objects.create(profile=instance)

#         elif instance.role == 'student':
#             # Adjust to your actual field name
#             StudentProfile.objects.create(student=instance)
# @receiver(post_save, sender=User)
# def create_related_profile(sender, instance, created, **kwargs):
#     if created:
#         StudentProfile.objects.create(student=instance)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not hasattr(instance, 'profile'):
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# ============================================================
# Group 1: Students, Courses & Grades
# ============================================================
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
# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     registration_number = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return f"{self.name} ({self.registration_number})"


class StudentProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student_profile")

    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ({self.registration_number})"
# class StudentProfile(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student_profile")
#     registration_number = models.CharField(max_length=20, unique=True)
#     year_of_study = models.IntegerField(default=1)
#     program = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.profile.user.username} ({self.registration_number})"

# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=10, unique=True)
#     credit_units = models.IntegerField(default=3)
#     lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecturer_courses')
# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=10)
#     lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User, related_name="enrolled_courses")
# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=10)
#     credit_units = models.IntegerField(default=3)  # <-- Add this line
#     lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(User, related_name="enrolled_courses")

#     def __str__(self):
#         return f"{self.code} - {self.name}"
# 
# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=10)
#     credit_units = models.IntegerField(default=3)
#     lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="taught_courses")
#     # students = models.ManyToManyField(User, related_name="enrolled_courses")
#     students = models.ManyToManyField(StudentProfile, related_name="enrolled_courses", blank=True)


#     def __str__(self):
#         return f"{self.code} - {self.name}"
class LecturerProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="lecturer_profile")
    department = models.CharField(max_length=100, blank=True, null=True)
    office_number = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} ({self.department or 'Lecturer'})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    credit_units = models.IntegerField(default=3)
    lecturer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="taught_courses"
    )
    students = models.ManyToManyField(StudentProfile, related_name="courses", blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

# =====================



# class StudentMark(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     score = models.FloatField()
#     grade = models.CharField(max_length=2, blank=True, null=True)
#     gpa = models.FloatField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         # Compute grade and GPA automatically
#         if self.score >= 80:
#             self.grade, self.gpa = 'A', 5.0
#         elif self.score >= 70:
#             self.grade, self.gpa = 'B+', 4.5
#         elif self.score >= 60:
#             self.grade, self.gpa = 'B', 4.0
#         elif self.score >= 50:
#             self.grade, self.gpa = 'C', 3.0
#         elif self.score >= 45:
#             self.grade, self.gpa = 'D', 2.0
#         else:
#             self.grade, self.gpa = 'F', 0.0
#         super().save(*args, **kwargs)

#     # def __str__(self):
#         # return f"{self.student.name} - {self.course.code}: {self.grade}"
#     def __str__(self):
#         return f"{self.student.username} - {self.course.code}: {self.grade}"
# at top of models.py
# class StudentMark(models.Model):
#     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     score = models.FloatField()
#     grade = models.CharField(max_length=2)
#     gpa = models.FloatField(blank=True, null=True, default=0.0)

# class StudentMark(models.Model):
#     student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="marks")
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     lecturer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="given_marks")
#     score = models.FloatField()
#     grade = models.CharField(max_length=2, blank=True, null=True)
#     gpa = models.FloatField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.student.username} - {self.course.code}: {self.grade}"

class StudentMark(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="marks")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="given_marks")
    score = models.FloatField()
    grade = models.CharField(max_length=2, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} ({self.score})"
# =====================
# STUDENT MARK MODEL
# =====================
# class StudentMark(models.Model):
#     student = models.ForeignKey(
#         "Profile",
#         limit_choices_to={"role": "student"},
#         on_delete=models.CASCADE,
#         related_name="student_marks"  #  unique related name
#     )

#     lecturer = models.ForeignKey(
#         "Profile",
#         limit_choices_to={"role": "lecturer"},
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="lecturer_marks"  #  unique related name
#     )

#     course = models.ForeignKey("Course", on_delete=models.CASCADE)
#     score = models.FloatField()
#     grade = models.CharField(max_length=2, blank=True)
#     gpa = models.FloatField(default=0)

#     def __str__(self):
#         return f"{self.student.user.username} - {self.course.name} ({self.score})"

# ============================================================
# Group 2: Student Life - Clubs & Activities
# ============================================================
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

    def __str__(self):
        return f"{self.title} ({self.club.name})"


# ============================================================
# Group 3: Careers & Internships
# ============================================================
class CareerOpportunity(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    deadline = models.DateField()
    link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.role}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)

class SavedOpportunity(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(CareerOpportunity, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# Group 4: Achievements & Endorsements
# ============================================================
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


# ============================================================
# Group 5: Support & Services
# ============================================================
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
