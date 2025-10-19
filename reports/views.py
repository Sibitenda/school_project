# reports/views.py
import io
import csv
import zipfile
import tempfile
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image as RLImage, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

from .forms import (
    SignUpForm, CourseForm, ClubForm,
    CareerOpportunityForm, AchievementForm, SupportTicketForm,
    AdminUserCreateForm, StudentMarkForm, AsyncReportForm
)
from .models import (
    Course, Club, CareerOpportunity,
    Achievement, SupportTicket, StudentMark, Profile
)

from reports.utils.grade_utils import (
    calculate_grade_and_gpa, calculate_gpa, calculate_cpa
)
from reports.utils.cloud_upload import push_all_to_cloud  # assumed available

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# -------------------------------
# Helpers
# -------------------------------
def build_student_report(student: Profile) -> Tuple[str, bytes]:
    """
    Build a single student's PDF report (in-memory) and return (filename, bytes).
    Uses reportlab + matplotlib. Safe for use in threads.
    """
    # gather marks
    marks_qs = StudentMark.objects.filter(student=student).select_related("course", "lecturer")
    marks = list(marks_qs)

    # compute summary numbers
    avg_gpa = round(calculate_gpa(marks), 2) if marks else 0.0
    cpa_val = calculate_cpa(student)

    # build PDF in memory
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Heading1"], alignment=1, spaceAfter=12)
    normal = styles["Normal"]

    # Header
    elements.append(Paragraph("Student Performance Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", normal))
    elements.append(Spacer(1, 12))

    student_name = getattr(student, "name", None) or getattr(student, "user", None)
    student_identifier = getattr(student, "registration_number", None) or getattr(student, "user", None)
    if hasattr(student_identifier, "username"):
        student_identifier = student_identifier.username
    elements.append(Paragraph(f"<b>Student:</b> {student_name}", normal))
    elements.append(Paragraph(f"<b>ID:</b> {student_identifier}", normal))
    elements.append(Spacer(1, 12))

    # Charts (create small images as in-memory buffers)
    chart_buffers = []

    if marks:
        try:
            # Score trend line
            plt.figure(figsize=(5.5, 2.5))
            courses = [m.course.name for m in marks]
            scores = [m.score for m in marks]
            plt.plot(courses, scores, marker='o', linestyle='-', color='#007acc')
            plt.title("Score Trend")
            plt.ylabel("Score (%)")
            plt.xticks(rotation=40, ha='right', fontsize=8)
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            chart_buffers.append(buf)
            plt.close()
        except Exception as e:
            logger.warning("Score trend chart failed for %s: %s", student, e)

        try:
            # Bar chart marks per course
            plt.figure(figsize=(5.5, 2.5))
            plt.bar(courses, scores, color="#2C7BE5")
            plt.title("Marks per Course")
            plt.ylabel("Score (%)")
            plt.xticks(rotation=40, ha='right', fontsize=8)
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            chart_buffers.append(buf)
            plt.close()
        except Exception as e:
            logger.warning("Bar chart failed for %s: %s", student, e)

    # GPA vs CPA chart (always)
    try:
        plt.figure(figsize=(3.5, 2.5))
        plt.bar(["GPA", "CPA"], [avg_gpa, cpa_val], color=["#4CAF50", "#2196F3"])
        plt.title("GPA vs CPA")
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        chart_buffers.append(buf)
        plt.close()
    except Exception as e:
        logger.warning("GPA/CPA chart failed for %s: %s", student, e)

    # embed charts
    for img_buf in chart_buffers:
        elements.append(RLImage(img_buf, width=420, height=160))
        elements.append(Spacer(1, 8))

    # summary
    total_courses = len(marks)
    elements.append(Paragraph(f"<b>Total Courses:</b> {total_courses}", normal))
    elements.append(Paragraph(f"<b>Average GPA:</b> {avg_gpa}", normal))
    elements.append(Paragraph(f"<b>Cumulative GPA (CPA):</b> {cpa_val}", normal))
    elements.append(Spacer(1, 12))

    # table of marks
    if marks:
        table_data = [["Course", "Score", "Grade", "GPA"]]
        for m in marks:
            try:
                grade, gpa_val = calculate_grade_and_gpa(m.score)
            except Exception:
                grade, gpa_val = getattr(m, "grade", ""), getattr(m, "gpa", None)
            table_data.append([
                getattr(m.course, "code", getattr(m.course, "name", str(m.course))),
                f"{m.score}",
                f"{grade}",
                f"{gpa_val:.2f}" if gpa_val is not None else "",
            ])
        t = Table(table_data, hAlign='LEFT', colWidths=[180, 60, 60, 60])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C7BE5")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No marks recorded.", normal))

    # finish PDF
    try:
        doc.build(elements)
    except Exception as e:
        logger.exception("Error building PDF for %s: %s", student, e)

    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    safe_name = str(student_name).replace(" ", "_")
    filename = f"{safe_name}.pdf"
    return filename, pdf_bytes


def send_report_email(student: Profile, filename: str, pdf_bytes: bytes) -> Tuple[bool, str]:
    """
    Send a single student's report as an email attachment.
    Returns (success, message).
    """
    user = getattr(student, "user", None)
    if not user:
        return False, "No linked user object"

    to_email = getattr(user, "email", None)
    if not to_email:
        return False, "No email address"

    subject = "Your Performance Report"
    body = f"Dear {getattr(user, 'username', '')},\n\nPlease find attached your performance report.\n\nRegards,\nAdmin"

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
            to=[to_email]
        )
        email.attach(filename, pdf_bytes, "application/pdf")
        email.send(fail_silently=False)
        return True, "Sent"
    except Exception as e:
        logger.exception("Email send failed for %s: %s", user, e)
        return False, str(e)


# -------------------------------
# Role checks & registration/redirects + dashboards (unchanged behavior)
# -------------------------------
def student_required(user):
    return hasattr(user, "profile") and user.profile.role == "student"


def lecturer_required(user):
    return hasattr(user, "profile") and user.profile.role == "lecturer"


def admin_required(user):
    return hasattr(user, "profile") and user.profile.role == "admin"


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get("role", "student")
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.name = getattr(user, "username", "")
            profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def home_redirect(request):
    profile = getattr(request.user, "profile", None)
    if not profile:
        return redirect("login")
    if profile.role == "student":
        return redirect("student_dashboard")
    if profile.role == "lecturer":
        return redirect("lecturer_dashboard")
    if profile.role == "admin":
        return redirect("admin_dashboard")
    return redirect("login")


@login_required
@user_passes_test(student_required)
def student_dashboard(request):
    profile = request.user.profile
    courses = Course.objects.filter(students=profile)
    achievements = Achievement.objects.filter(student=profile)
    tickets = SupportTicket.objects.filter(student=profile)
    marks = StudentMark.objects.filter(student=profile)
    gpa = calculate_gpa(marks)
    cpa = calculate_cpa(profile)
    return render(request, "student_dashboard.html", {
        "profile": profile,
        "courses": courses,
        "achievements": achievements,
        "tickets": tickets,
        "marks": marks,
        "gpa": gpa,
        "cpa": cpa,
    })


@login_required
@user_passes_test(lecturer_required)
def lecturer_dashboard(request):
    profile = request.user.profile
    try:
        courses = Course.objects.filter(lecturer=profile)
    except Exception:
        courses = Course.objects.filter(lecturer=request.user)
    return render(request, "lecturer_dashboard.html", {"profile": profile, "courses": courses})


# -------------------------------
# Admin Dashboard (main)
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
        "student_mark_form": StudentMarkForm(),
        "async_report_form": AsyncReportForm(),
    }

    # preload data
    marks = StudentMark.objects.select_related("student", "course").all()
    students = Profile.objects.filter(role="student")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_user":
            form = AdminUserCreateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "User created.")
                return redirect("admin_dashboard")
            forms["user_form"] = form

        elif action == "delete_user":
            profile_id = request.POST.get("profile_id")
            if profile_id:
                Profile.objects.filter(id=profile_id).delete()
                messages.success(request, "User deleted.")
                return redirect("admin_dashboard")

        elif action == "course_form":
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, "Course added.")
                return redirect("admin_dashboard")
            forms["course_form"] = course_form

        elif action == "student_mark_form":
            student_mark_form = StudentMarkForm(request.POST)
            if student_mark_form.is_valid():
                mark = student_mark_form.save(commit=False)
                mark.grade, mark.gpa = calculate_grade_and_gpa(mark.score)
                mark.save()
                messages.success(request, "Student mark recorded.")
                return redirect("admin_dashboard")
            forms["student_mark_form"] = student_mark_form

        elif action == "update_ticket_status":
            ticket_id = request.POST.get("ticket_id")
            new_status = request.POST.get("status")
            if ticket_id and new_status:
                SupportTicket.objects.filter(id=ticket_id).update(status=new_status)
                messages.success(request, "Ticket status updated.")
                return redirect("admin_dashboard")

        elif action == "export_marks_csv":
            return export_marks_csv(request)

        elif action == "generate_student_reports_zip":
            return generate_student_reports_zip(request)

        elif action == "send_all_reports_email":
            # Manual action: generate & send emails to all students (not inside threaded ZIP)
            return send_all_reports_email(request)

    # refresh summaries for display
    marks = StudentMark.objects.select_related("student", "course").all()
    for mark in marks:
        try:
            mark.grade, mark.gpa = calculate_grade_and_gpa(mark.score)
        except Exception:
            mark.grade = getattr(mark, "grade", "")
            mark.gpa = getattr(mark, "gpa", None)
        try:
            mark.cpa = calculate_cpa(mark.student)
        except Exception:
            mark.cpa = None

    for s in students:
        s.gpa = calculate_gpa(StudentMark.objects.filter(student=s))
        try:
            s.cpa = calculate_cpa(s)
        except Exception:
            s.cpa = None

    context = forms
    context.update({
        "students": students,
        "lecturers": Profile.objects.filter(role="lecturer"),
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
        student_name = getattr(mark.student, "name", None) or getattr(mark.student, "user", None)
        if hasattr(student_name, "username"):
            student_name = student_name.username
        writer.writerow([
            student_name,
            getattr(mark.course, "name", str(mark.course)),
            mark.score,
            grade,
            f"{gpa:.2f}"
        ])
    return response


# -------------------------------
# Download Processed Marksheet (concurrent)
# -------------------------------
@login_required
@user_passes_test(admin_required)
def download_processed_marks_csv(request):
    import pandas as pd
    import threading

    def process_student_marks_concurrent(df):
        results = []

        def compute_row(idx, row):
            try:
                grade, gpa_val = calculate_grade_and_gpa(row["score"])
                row["grade"] = grade
                row["gpa"] = gpa_val
                row["cpa"] = calculate_cpa(row["student"])
                results.append(row)
            except Exception as e:
                logger.exception("Error computing row: %s", e)

        threads = []
        for i, (_, row) in enumerate(df.iterrows()):
            t = threading.Thread(target=compute_row, args=(i, row))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return pd.DataFrame(results)

    marks = StudentMark.objects.select_related("student__user", "course", "lecturer").all()
    data = []
    for mark in marks:
        data.append({
            "student": mark.student,
            "course": getattr(mark.course, "name", str(mark.course)),
            "lecturer": getattr(mark.lecturer, "name", str(mark.lecturer)) if mark.lecturer else "",
            "score": mark.score,
        })

    if not data:
        messages.error(request, "No marks available to export.")
        return redirect("admin_dashboard")

    df = pd.DataFrame(data)
    processed_df = process_student_marks_concurrent(df)

    # rename for tidy export
    processed_df = processed_df.rename(columns={"student": "Student", "course": "Course", "lecturer": "Lecturer",
                                                "score": "Score", "grade": "Grade", "gpa": "GPA", "cpa": "CPA"})
    csv_buffer = io.StringIO()
    processed_df.to_csv(csv_buffer, index=False)
    response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="processed_marks.csv"'
    return response


# -------------------------------
# Generate reports (ZIP) - threaded, does NOT email inside threads
# -------------------------------
@login_required
@user_passes_test(admin_required)
def generate_student_reports_zip(request):
    start_time = time.time()
    students = Profile.objects.filter(role="student")
    if not students.exists():
        messages.error(request, "No students to report.")
        return redirect("admin_dashboard")

    logger.info("Starting threaded report generation for %d students", students.count())
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(build_student_report, s): s for s in students}
            for fut in as_completed(futures):
                student = futures[fut]
                try:
                    filename, pdf_bytes = fut.result()
                    zip_file.writestr(filename, pdf_bytes)
                except Exception as e:
                    logger.exception("Failed to build report for %s: %s", student, e)

    elapsed = time.time() - start_time
    logger.info("Completed report generation in %.2f seconds", elapsed)

    zip_buffer.seek(0)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    zip_filename = f"student_reports_{timestamp}.zip"
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'

    # Try uploading to cloud (best-effort). We pass name; your push_all_to_cloud may expect a path or name.
    try:
        async_to_sync(push_all_to_cloud)(zip_filename)
        messages.success(request, "Reports generated and uploaded to cloud (attempted).")
    except Exception as e:
        logger.exception("Cloud upload failed: %s", e)
        messages.warning(request, f"Reports generated but cloud upload failed: {e}")

    return response


# -------------------------------
# Manual: Generate & Send all reports by email (triggered by button)
# -------------------------------
@login_required
@user_passes_test(admin_required)
def send_all_reports_email(request):
    """
    Generates each student's PDF and sends it by email.
    This is a manual action (triggered from admin_dashboard) to avoid mixing emails into threaded ZIP generation.
    """
    students = Profile.objects.filter(role="student")
    if not students.exists():
        messages.error(request, "No students to email.")
        return redirect("admin_dashboard")

    successes = []
    failures = []

    for student in students:
        try:
            filename, pdf_bytes = build_student_report(student)
            ok, msg = send_report_email(student, filename, pdf_bytes)
            if ok:
                successes.append(student.user.username if hasattr(student, "user") else str(student))
            else:
                failures.append(f"{getattr(student.user, 'username', str(student))}: {msg}")
        except Exception as e:
            logger.exception("Failed sending report for %s: %s", student, e)
            failures.append(f"{getattr(student.user, 'username', str(student))}: {e}")

    if successes:
        messages.success(request, f"Sent {len(successes)} emails successfully.")
    if failures:
        messages.warning(request, f"Failed sending to: {', '.join(failures[:10])}" + (f" (+{len(failures)-10} more)" if len(failures) > 10 else ""))

    return redirect("admin_dashboard")
