"""medimageshub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from . import views

admin.site.site_header = "MedimagesHub administration"
admin.site.site_title = "MedimagesHub administration"
admin.site.index_title = "Admin dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path('', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('images/', include('dicoms.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)