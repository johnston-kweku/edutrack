from django.urls import path
from . import views


app_name = 'students'
urlpatterns = [
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('detail/<str:student_id>/', views.student_detail, name='student_detail'),
    path('attendance/mark/<int:class_id>/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('student/add/', views.add_student, name='add_student'),
    path('attendance/form/', views.mark_attendance_form, name='attendance_form'),
    path('student/attendance/<str:student_id>/', views.per_student_attendance, name='per_student_attendance'),
    path('student/fee/history/<str:student_id>/', views.student_fee_payment_history, name='fee_payment_history'),
]