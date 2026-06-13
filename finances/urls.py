from django.urls import path
from . import views
app_name = 'finances'

urlpatterns = [
    path('dashboard/summary/', views.dashboard_summary, name='dashboard_summary'),
]