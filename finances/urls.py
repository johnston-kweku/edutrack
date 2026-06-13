from django.urls import path
from django.conf import settings
from . import views
app_name = 'finances'

def sentry_trigger(request):
    1/0

urlpatterns = [
    path('dashboard/summary/', views.dashboard_summary, name='dashboard_summary'),
]

if settings.DEBUG:
    urlpatterns.append(path('sentry-trigger/', sentry_trigger))