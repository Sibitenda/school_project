from django import forms
from django.contrib.auth.models import User
from .models import (
    Profile, Course, StudentMark, CourseReview,
    Club, ClubPost,
    CareerOpportunity, SavedOpportunity,
    Achievement, Endorsement,
    SupportTicket, TicketResponse,
)


# ============================================================
# Group 0: User & Registration
# ============================================================
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
            # Default role = student
            Profile.objects.create(user=user, role="student", name=user.username)
        return user


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
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.name = self.cleaned_data["name"]
            profile.role = self.cleaned_data["role"]
            profile.save()
        return user


# ============================================================
# Group 1: Academic Models
# ============================================================
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
            lambda obj: f"{obj.name} ({obj.user.username})"
        )
        self.fields["lecturer"].label_from_instance = (
            lambda obj: f"{obj.name} ({obj.user.username})"
        )
        self.fields["course"].label_from_instance = (
            lambda obj: f"{obj.code} - {obj.name}"
        )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "credit_units", "lecturer", "students"]
        widgets = {
            "students": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = Profile.objects.filter(role="lecturer")
        self.fields["students"].queryset = Profile.objects.filter(role="student")

        self.fields["lecturer"].label_from_instance = (
            lambda obj: f"{obj.name} ({obj.user.username})"
        )
        self.fields["students"].label_from_instance = (
            lambda obj: f"{obj.name} ({obj.user.username})"
        )


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ["course", "student", "rating", "comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Profile.objects.filter(role="student")


# ============================================================
# Group 2: Clubs & Student Life
# ============================================================
class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description", "meeting_time", "members"]
        widgets = {"members": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = Profile.objects.filter(role="student")


class ClubPostForm(forms.ModelForm):
    class Meta:
        model = ClubPost
        fields = ["club", "author", "title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].queryset = Profile.objects.all()


# ============================================================
# Group 3: Careers & Internships
# ============================================================
class CareerOpportunityForm(forms.ModelForm):
    class Meta:
        model = CareerOpportunity
        fields = ["company", "role", "deadline", "link"]


class SavedOpportunityForm(forms.ModelForm):
    class Meta:
        model = SavedOpportunity
        fields = ["student", "opportunity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Profile.objects.filter(role="student")


# ============================================================
# Group 4: Achievements & Endorsements
# ============================================================
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ["student", "title", "description", "is_public"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Profile.objects.filter(role="student")


class EndorsementForm(forms.ModelForm):
    class Meta:
        model = Endorsement
        fields = ["achievement", "endorsed_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["endorsed_by"].queryset = Profile.objects.all()


# ============================================================
# Group 5: Support & Services
# ============================================================
class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["student", "title", "description", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Profile.objects.filter(role="student")


class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ["ticket", "responder", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["responder"].queryset = Profile.objects.all()


# ============================================================
# Group 6: Async Reports
# ============================================================
class AsyncReportForm(forms.Form):
    """Simple form to trigger asynchronous student report generation."""
    trigger = forms.BooleanField(widget=forms.HiddenInput, initial=True)
