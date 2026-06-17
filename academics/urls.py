from django.urls import path
from . import views
app_name = 'academics'

urlpatterns = [
    path('classes/', views.classes_list, name='classes_list'),
    path('class/<int:class_id>/', views.class_view, name='class'),
    path('list/teachers/', views.teachers_view, name='teachers_list'),
    path('add/student/', views.add_student, name='add_student'),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('class/add/', views.add_class, name='add_class'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('class/edit/<int:class_id>/', views.edit_class, name='edit_class')
]