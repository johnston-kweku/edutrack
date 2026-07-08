from django.urls import path
from django.conf import settings
from . import views
app_name = 'finances'

def sentry_trigger(request):
    1/0

urlpatterns = [
    path('dashboard/summary/', views.dashboard_summary, name='dashboard_summary'),
    path('add/fee/', views.add_fee, name='add_fee'),
    path('finances/', views.finances_view, name='finances'),
    path('fee/payment/', views.record_fee_payment, name='fee_payment'),
    path('api/students-by-fee/', views.get_students_by_fee, name='get_students_by_fee'),
    path('fee/class/<int:fee_id>/',  views.class_fee_detail, name='class_detail')
]

if settings.DEBUG:
    urlpatterns.append(path('sentry-trigger/', sentry_trigger))