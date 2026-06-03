from django.urls import path
from . import views

urlpatterns = [
    path('class/<int:class_id>/', views.students_list_per_class, name='students_list_per_class'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('detail/<int:student_id>/', views.student_detail, name='student_detail'),
]