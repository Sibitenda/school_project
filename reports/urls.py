
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
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("lecturer/", views.lecturer_dashboard, name="lecturer_dashboard"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("", views.home_redirect, name="home"),
]
