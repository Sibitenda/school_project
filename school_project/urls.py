from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("reports.urls")),          # your app first
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("admin/", admin.site.urls),            # admin panel last
    
]
