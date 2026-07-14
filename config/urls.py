"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403, handler400
from dashboards import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('finances/', include('finances.urls')),
    path('students/', include('students.urls')),
    path('dashboard/', include('dashboards.urls')),
]

if not settings.DEBUG:
    urlpatterns.append(re_path(r'^.*$', dashboard_views.catch_all_404, name='catch_all_404'))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if not settings.DEBUG:
    handler404 = 'dashboards.views.handle_404'
    handler500 = 'dashboards.views.handle_500'
    handler403 = 'dashboards.views.handle_403'