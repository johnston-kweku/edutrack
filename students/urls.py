from django.urls import path
from . import views


app_name = 'students'
urlpatterns = [
    path('class/<int:class_id>/', views.students_list_per_class, name='students_list_per_class'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('detail/<str:student_id>/', views.student_detail, name='student_detail'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('student/add/', views.add_student, name='add_student')
]