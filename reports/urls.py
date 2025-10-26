from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Home / Redirects
    path("", views.home_redirect, name="home"),

    # Dashboards
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),

    # Authentication & Registration
    path("register/", views.register, name="register"),

    # Admin utilities
    path("admin/send-emails/", views.send_all_reports_email, name="send_all_reports_email"),
    path("admin/generate-zip/", views.generate_student_reports_zip, name="generate_student_reports_zip"),
    path("admin/download-processed/", views.download_processed_marks_csv, name="download_processed_marks_csv"),

    # API endpoints
    # Include the API routes (reports/api/urls.py)
    path("api/", include("reports.api.urls")),

    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/dashboard/", views.dashboard, name="dashboard"),

]
