# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("", include("reports.urls")),          # your app first
#     path("accounts/", include("django.contrib.auth.urls")),  # login/logout
#     path("admin/", admin.site.urls),            # admin panel last
    
# ]
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('reports.urls')),  #  make reports URLs root-level
# ]

from django.contrib import admin
from django.urls import path, include
from reports.views import home_redirect

urlpatterns = [
    path('', home_redirect, name="home"),
    path('admin/', admin.site.urls),
    path('', include('reports.urls')),
]

