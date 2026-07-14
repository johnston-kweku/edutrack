from django.urls import path
from . import views

app_name = 'dashboards'
urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('parents/', views.parents_dashboard, name='parents_dashboard')
]