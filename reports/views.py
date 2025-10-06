from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.http import HttpResponse
import csv

from .forms import (
    SignUpForm, StudentForm, CourseForm, ClubForm,
    CareerOpportunityForm, AchievementForm, SupportTicketForm,
    AdminUserCreateForm, StudentMarkForm
)
from .models import (
    Student, Course, Club, CareerOpportunity,
    Achievement, SupportTicket, StudentMark, Profile
)
from reports.utils.grade_utils import (
    get_letter_grade, calculate_gpa, calculate_cpa
)

from .models import (
    Student, Course, Club, CareerOpportunity,
    Achievement, SupportTicket, StudentMark,
    Profile, StudentProfile, LecturerProfile
)
from reports.utils.grade_utils import calculate_grade_and_gpa
from reports.utils.calculations import average


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

            role = request.POST.get("role", "student")
            if hasattr(user, "profile"):
                user.profile.role = role
                user.profile.save()

            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})


# -------------------------------
# Role-based Redirect
# -------------------------------
@login_required
def home_redirect(request):
    """Redirect user to their dashboard based on role."""
    if request.user.is_authenticated:
        if hasattr(request.user, "profile"):
            if request.user.profile.role == "student":
                return redirect("student_dashboard")
            elif request.user.profile.role == "lecturer":
                return redirect("lecturer_dashboard")
            elif request.user.profile.role == "admin":
                return redirect("admin_dashboard")
    return redirect("login")  # fallback


# -------------------------------
# Student Dashboard
# -------------------------------
@login_required
@user_passes_test(student_required)
def student_dashboard(request):
    user = request.user
    profile = user.profile

    # courses = Course.objects.filter(students=user)
    # achievements = Achievement.objects.filter(student=user)
    # tickets = SupportTicket.objects.filter(student=user)
    # marks = StudentMark.objects.filter(student=user)
    student_profile = StudentProfile.objects.get(user=request.user)

    courses = Course.objects.filter(students=student_profile)
    achievements = Achievement.objects.filter(student=student_profile)
    tickets = SupportTicket.objects.filter(student=student_profile)
    marks = StudentMark.objects.filter(student=student_profile)


    gpa = calculate_gpa(marks)
    cpa = calculate_cpa(profile)

    return render(request, "./student_dashboard.html", {
        "profile": profile,
        "courses": courses,
        "achievements": achievements,
        "tickets": tickets,
        "marks": marks,
        "gpa": gpa,
        "cpa": cpa,
    })


# -------------------------------
# Lecturer Dashboard
# -------------------------------
@login_required
@user_passes_test(lecturer_required)
def lecturer_dashboard(request):
    user = request.user
    profile = user.profile

    # Correct relationship lookup
    lecturer_profile = LecturerProfile.objects.get(profile__user=request.user)

    courses = Course.objects.filter(lecturer=request.user)

    return render(request, "lecturer_dashboard.html", {
        "profile": profile,
        "lecturer_profile": lecturer_profile,
        "courses": courses,
    })



# -------------------------------
# Admin Dashboard
# -------------------------------
@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    # Initialize forms
    forms = {
        "user_form": AdminUserCreateForm(),
        "course_form": CourseForm(),
        "club_form": ClubForm(),
        "opportunity_form": CareerOpportunityForm(),
        "achievement_form": AchievementForm(),
        "ticket_form": SupportTicketForm(),
        "student_mark_form": StudentMarkForm(),
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_user":
            form = AdminUserCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("admin_dashboard")
            forms["user_form"] = form

        elif action == "delete_user":
            profile_id = request.POST.get("profile_id")
            if profile_id:
                Profile.objects.filter(id=profile_id).delete()
                return redirect("admin_dashboard")

        # elif action == "student_mark_form":
        #     mark_form = StudentMarkForm(request.POST)
        #     if mark_form.is_valid():
        #         mark_form.save()
        #         return redirect("admin_dashboard")
        #     forms["student_mark_form"] = mark_form
        # Add Course
        elif action == "course_form":
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect("admin_dashboard")

        elif action == "student_mark_form":
            student_mark_form = StudentMarkForm(request.POST)
            if student_mark_form.is_valid():
                mark = student_mark_form.save(commit=False)

                # --- Calculate grade & GPA from utils ---
                mark.grade, mark.gpa = calculate_grade_and_gpa(mark.score)

                mark.save()

                # update CPA for the student
                student = mark.student
                student.cpa = calculate_cpa(student)
                student.save()

                return redirect("admin_dashboard")
            forms["student_mark_form"] = student_mark_form

        

        elif action == "update_ticket_status":
            ticket_id = request.POST.get("ticket_id")
            new_status = request.POST.get("status")
            if ticket_id and new_status:
                SupportTicket.objects.filter(id=ticket_id).update(status=new_status)
                return redirect("admin_dashboard")

        elif action == "export_marks_csv":
            return export_marks_csv(request)

    # # Compute grades and GPA for all students
    # marks = StudentMark.objects.select_related("student", "course").all()
    # for mark in marks:
    #     mark.grade = get_letter_grade(mark.score)
    #     mark.gpa = calculate_gpa(StudentMark.objects.filter(student=mark.student))

    # #  FIX HERE — use StudentProfile instead of Profile
    # students = StudentProfile.objects.all()
    # for s in students:
    #     s.gpa = calculate_gpa(StudentMark.objects.filter(student=s))
    #     s.cpa = calculate_cpa(s)
    # Compute grades and GPA for all marks
    marks = StudentMark.objects.select_related("student", "course").all()
    for mark in marks:
        mark.grade, mark.gpa = calculate_grade_and_gpa(mark.score)

    # Compute GPA/CPA per student
    students = StudentProfile.objects.all()
    for s in students:
        s.gpa = calculate_gpa(StudentMark.objects.filter(student=s))
        s.cpa = calculate_cpa(s)

    context = forms
    context.update({
        "students": students,
        "lecturers": LecturerProfile.objects.all(),
        "admins": Profile.objects.filter(role="admin"),
        "courses": Course.objects.all(),
        "clubs": Club.objects.all(),
        "opportunities": CareerOpportunity.objects.all(),
        "achievements": Achievement.objects.all(),
        "tickets": SupportTicket.objects.all(),
        "marks": marks,
    })

    return render(request, "admin_dashboard.html", context)


# -------------------------------
# Export Marks CSV
# -------------------------------
@login_required
@user_passes_test(admin_required)
def export_marks_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="student_marks.csv"'

    writer = csv.writer(response)
    writer.writerow(["Student", "Course", "Score", "Grade", "GPA"])

    marks = StudentMark.objects.select_related("student", "course").all()
    for mark in marks:
        grade, gpa = calculate_grade_and_gpa(mark.score)
        writer.writerow([
            mark.student.user.username,
            mark.course.name,
            mark.score,
            grade,
            f"{gpa:.2f}"
        ])

    return response

# -------------------------------
# Export All Data CSV (NEW)
# -------------------------------
@login_required
@user_passes_test(admin_required)
def export_all_data_csv(request):
    """Exports all key tables (Students, Lecturers, Courses, Clubs, Opportunities, Achievements, Tickets) into one CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="school_data_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["=== STUDENTS ==="])
    writer.writerow(["Name", "Email", "GPA", "CPA"])
    for s in Profile.objects.filter(role="student"):
        writer.writerow([s.name, s.user.email if s.user else "", calculate_gpa(StudentMark.objects.filter(student=s)), calculate_cpa(s)])

    writer.writerow([])
    writer.writerow(["=== LECTURERS ==="])
    writer.writerow(["Name", "Email"])
    for l in Profile.objects.filter(role="lecturer"):
        writer.writerow([l.name, l.user.email if l.user else ""])

    writer.writerow([])
    writer.writerow(["=== COURSES ==="])
    writer.writerow(["Code", "Name", "Lecturer", "Students"])
    for c in Course.objects.all():
        student_names = ", ".join([s.user.username for s in c.students.all()])
        writer.writerow([c.code, c.name, c.lecturer, student_names])

    writer.writerow([])
    writer.writerow(["=== CLUBS ==="])
    writer.writerow(["Name", "Description"])
    for club in Club.objects.all():
        writer.writerow([club.name, club.description])

    writer.writerow([])
    writer.writerow(["=== CAREER OPPORTUNITIES ==="])
    writer.writerow(["Company", "Role", "Deadline"])
    for o in CareerOpportunity.objects.all():
        writer.writerow([o.company, o.role, o.deadline])

    writer.writerow([])
    writer.writerow(["=== ACHIEVEMENTS ==="])
    writer.writerow(["Student", "Title", "Description"])
    for a in Achievement.objects.all():
        writer.writerow([a.student, a.title, a.description])

    writer.writerow([])
    writer.writerow(["=== SUPPORT TICKETS ==="])
    writer.writerow(["Student", "Title", "Status"])
    for t in SupportTicket.objects.all():
        writer.writerow([t.student, t.title, t.status])

    return response
