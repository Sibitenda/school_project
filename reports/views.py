from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .forms import SignUpForm, StudentForm, CourseForm, ClubForm, CareerOpportunityForm, AchievementForm, SupportTicketForm
from .models import Student, Course, Club, CareerOpportunity, Achievement, SupportTicket
from .forms import AdminUserCreateForm
from .models import Profile
# -------------------------------
# Role Checks
# -------------------------------
def student_required(user):
    return hasattr(user, "profile") and user.profile.role == "student"

def lecturer_required(user):
    return hasattr(user, "profile") and user.profile.role == "lecturer"

def admin_required(user):
    return hasattr(user, "profile") and user.profile.role == "admin"

# -------------------------------
# Registration
# -------------------------------
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get role from the dropdown in register.html
            role = request.POST.get("role", "student")  # default student
            if hasattr(user, "profile"):
                user.profile.role = role
                user.profile.save()

            # Log user in immediately
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form})

# -------------------------------
# Role-based Redirect (after login)
# -------------------------------
@login_required
def home_redirect(request):
    """Send user to dashboard based on profile.role"""
    role = getattr(request.user.profile, "role", None)

    if role == "student":
        return redirect("student_dashboard")
    elif role == "lecturer":
        return redirect("lecturer_dashboard")
    elif role == "admin":
        return redirect("admin_dashboard")
    else:
        return redirect("login")  # fallback if no role

# -------------------------------
# Student Dashboard
# -------------------------------
# @login_required
# @user_passes_test(student_required)
# def student_dashboard(request):
#     return render(request, "student_dashboard.html", {
#         "courses": Course.objects.filter(students__profile__user=request.user),
#         "tickets": SupportTicket.objects.filter(student__profile__user=request.user),
#     })
# @login_required
# @user_passes_test(student_required)
# def student_dashboard(request):
#     profile = request.user.profile

#     courses = Course.objects.filter(students=profile)
#     achievements = Achievement.objects.filter(student=profile)
#     tickets = SupportTicket.objects.filter(student=profile)

#     return render(request, "reports/student_dashboard.html", {
#         "profile": profile,
#         "courses": courses,
#         "achievements": achievements,
#         "tickets": tickets,
#     })
@login_required
@user_passes_test(student_required)
def student_dashboard(request):
    user = request.user  # actual User object
    profile = user.profile

    courses = Course.objects.filter(students=user)  
    achievements = Achievement.objects.filter(student=user)  
    tickets = SupportTicket.objects.filter(student=user)  

    return render(request, "./student_dashboard.html", {
        "profile": profile,
        "courses": courses,
        "achievements": achievements,
        "tickets": tickets,
    })

# -------------------------------
# Lecturer Dashboard
# -------------------------------
@login_required
@user_passes_test(lecturer_required)
def lecturer_dashboard(request):
    return render(request, "lecturer_dashboard.html", {
        "courses": Course.objects.filter(lecturer=request.user.username),
    })

# -------------------------------
# Admin Dashboard
# -------------------------------

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    forms = {
        "user_form": AdminUserCreateForm(),
        "course_form": CourseForm(),
        "club_form": ClubForm(),
        "opportunity_form": CareerOpportunityForm(),
        "achievement_form": AchievementForm(),
        "ticket_form": SupportTicketForm(),
    }

    if request.method == "POST":
        action = request.POST.get("action")

        # -------- Create User --------
        if action == "create_user":
            form = AdminUserCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("admin_dashboard")
            else:
                forms["user_form"] = form

        # -------- Delete Any User --------
        elif action == "delete_user":
            profile_id = request.POST.get("profile_id")
            if profile_id:
                Profile.objects.filter(id=profile_id).delete()
                return redirect("admin_dashboard")

        # -------- Handle Other Forms (courses, clubs, etc.) --------
        elif action in forms:
            form_class = forms[action].__class__
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect("admin_dashboard")
        elif action == "update_ticket_status":
            ticket_id = request.POST.get("ticket_id")
            new_status = request.POST.get("status")
            if ticket_id and new_status:
                SupportTicket.objects.filter(id=ticket_id).update(status=new_status)
                return redirect("admin_dashboard")

            else:
                forms[action] = form  # keep errors visible

    context = forms
    context.update({
        "students": Profile.objects.filter(role="student"),
        "lecturers": Profile.objects.filter(role="lecturer"),
        "admins": Profile.objects.filter(role="admin"),
        "courses": Course.objects.all(),
        "clubs": Club.objects.all(),
        "opportunities": CareerOpportunity.objects.all(),
        "achievements": Achievement.objects.all(),
        "tickets": SupportTicket.objects.all(),
    })
    return render(request, "./admin_dashboard.html", context)

