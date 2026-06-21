from django.urls import path
from . import views


app_name = 'students'
urlpatterns = [
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('detail/<str:student_id>/', views.student_detail, name='student_detail'),
    path('attendance/mark/<int:class_id>/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('student/add/', views.add_student, name='add_student'),
    path('attendance/form/', views.mark_attendance_form, name='attendance_form')
]