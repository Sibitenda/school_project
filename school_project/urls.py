# from django.contrib import admin
# from django.urls import path, include
# # urlpatterns = [
# #     path("admin/", admin.site.urls),
# #     path("", include("reports.urls")),  # all app routes handled inside reports/urls.py
# # ]
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("reports.urls")),   # your app routes
#     path("accounts/", include("django.contrib.auth.urls")),  # ✅ login/logout
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import redirect

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('dashboard/', include('reports.urls')),  # replace 'yourapp' with your app name
#     path('accounts/', include('django.contrib.auth.urls')),

#     # Redirect root URL to dashboard
#     path('', lambda request: redirect('dashboard')),
# ]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("reports.urls")),          # your app first
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("admin/", admin.site.urls),            # admin panel last
]
