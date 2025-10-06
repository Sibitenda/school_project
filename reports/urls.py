
# # from django.contrib import admin
# # from django.urls import path
# # from . import views

# # # urlpatterns = [
# # #     path("", views.dashboard, name="dashboard"),
# # # ]
# # urlpatterns = [
# #     path("dashboard/", views.redirect_dashboard, name="dashboard"),
# #     path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
# #     path("dashboard/lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
# #     path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
# # ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.home_redirect, name="home"),
#     path("student/", views.student_dashboard, name="student_dashboard"),
#     path("lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
#     path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
#     path("register/", views.register, name="register"),
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path("register/", views.register, name="register"),
#     path("student/", views.student_dashboard, name="student_dashboard"),
#     path("lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
#     path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
#     path("", views.home_redirect, name="home"),
#     # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     # path('export-students-csv/', views.export_students_csv, name='export_students_csv'),
#     path('export-all-data-csv/', views.export_all_data_csv, name='export_all_data_csv'),

    

# ]
from django.urls import path
from . import views

urlpatterns = [
    # Home / Redirects
    path("", views.home_redirect, name="home"),

    # Dashboards
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),  # cleaner URL

    # Authentication & Registration
    path("register/", views.register, name="register"),

    # Data Export
    path("export/all-data-csv/", views.export_all_data_csv, name="export_all_data_csv"),
    # path("export/all-data-csv/", views.export_marks_csv, name="export_all_data_csv"),

    # path("export/students-csv/", views.export_students_csv, name="export_students_csv"),  # enable later if needed
]

