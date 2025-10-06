from django import forms
from django.contrib.auth.models import User
from .models import (
    Student, Grade, StudentMark,
    Course, CourseReview,
    Club, ClubPost,
    CareerOpportunity, SavedOpportunity,
    Achievement, Endorsement,
    SupportTicket, TicketResponse,
)

from .models import Profile
from .models import Course, StudentProfile, StudentMark
# -------------------------------
# Group 0: Students & Grades
# -------------------------------
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile', 'name', 'email']  # include the fields you want

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["student", "subject", "score"]

# class StudentMarkForm(forms.ModelForm):
#     class Meta:
#         model = StudentMark
#         fields = ["student", "course", "score"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Populate students and courses
#         self.fields["student"].queryset = StudentProfile.objects.all()
#         self.fields["course"].queryset = Course.objects.all()

#         self.fields["student"].label_from_instance = (
#             lambda obj: f"{obj.name} ({obj.registration_number})"
#         )
#         self.fields["course"].label_from_instance = (
#             lambda obj: f"{obj.name} ({obj.code})"
#         )
# -------------------------------
# Group 0: Students & Grades
# -------------------------------
# class StudentMarkForm(forms.ModelForm):
#     class Meta:
#         model = StudentMark
#         fields = ["student", "course", "lecturer", "score"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         from .models import Profile, Course

#         self.fields["student"].queryset = Profile.objects.filter(role="student")
#         self.fields["lecturer"].queryset = Profile.objects.filter(role="lecturer")
#         self.fields["course"].queryset = Course.objects.all()

#         # self.fields["student"].label_from_instance = lambda obj: f"{obj.name} ({obj.user.username})"
#         # self.fields["lecturer"].label_from_instance = lambda obj: f"{obj.name} ({obj.user.username})"
#         # self.fields["course"].label_from_instance = lambda obj: f"{obj.name} ({obj.code})"

#         self.fields["student"].label_from_instance = lambda obj: f"{getattr(obj, 'name', obj.user.username)} ({obj.user.username})"
#         self.fields["lecturer"].label_from_instance = lambda obj: f"{getattr(obj, 'name', obj.user.username)} ({obj.user.username})"
#         self.fields["course"].label_from_instance = lambda obj: f"{obj.name} ({obj.code})"
class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ["student", "course", "lecturer", "score"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Profile, Course

        self.fields["student"].queryset = Profile.objects.filter(role="student")
        self.fields["lecturer"].queryset = Profile.objects.filter(role="lecturer")
        self.fields["course"].queryset = Course.objects.all()

        self.fields["student"].label_from_instance = (
            lambda obj: f"{obj.user.username}"
        )
        self.fields["lecturer"].label_from_instance = (
            lambda obj: f"{obj.user.username}"
        )
        self.fields["course"].label_from_instance = (
            lambda obj: f"{obj.code} - {obj.name}"
        )

class AdminUserCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[
        ("student", "Student"),
        ("lecturer", "Lecturer"),
        ("admin", "Admin"),
    ])

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create/update profile with role + name
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data["role"]
            profile.name = self.cleaned_data["name"]
            profile.save()
        return user

# class StudentSignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#             Profile.objects.create(user=user, role="student")
#         return user

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.create(user=user, role="student")
        return user


# -------------------------------
# Group 1: Courses & Enrollment
# -------------------------------
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ["name", "code", "credit_units", "lecturer", "students"]
#         widgets = {"students": forms.CheckboxSelectMultiple}
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ["name", "code", "lecturer", "students"]
#         widgets = {"students": forms.CheckboxSelectMultiple}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "credit_units", "lecturer", "students"]
        widgets = {
            "students": forms.CheckboxSelectMultiple,  # ✅ shows all students as checkboxes
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter only student users (if you have a Profile with role='student')
        self.fields["students"].queryset = User.objects.filter(profile__role="student")

class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ["course", "student", "rating", "comment"]


# -------------------------------
# Group 2: Clubs & Student Life
# -------------------------------
class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description", "meeting_time", "members"]
        widgets = {"members": forms.CheckboxSelectMultiple}

class ClubPostForm(forms.ModelForm):
    class Meta:
        model = ClubPost
        fields = ["club", "author", "title", "content"]


# -------------------------------
# Group 3: Careers & Internships
# -------------------------------
class CareerOpportunityForm(forms.ModelForm):
    class Meta:
        model = CareerOpportunity
        fields = ["company", "role", "deadline", "link"]

class SavedOpportunityForm(forms.ModelForm):
    class Meta:
        model = SavedOpportunity
        fields = ["student", "opportunity"]


# -------------------------------
# Group 4: Achievements & Profiles
# -------------------------------
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ["student", "title", "description", "is_public"]

class EndorsementForm(forms.ModelForm):
    class Meta:
        model = Endorsement
        fields = ["achievement", "endorsed_by"]


# -------------------------------
# Group 5: Support & Services
# -------------------------------
class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["student", "title", "description", "status"]

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ["ticket", "responder", "message"]
