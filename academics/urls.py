from django.urls import path
from . import views
app_name = 'academics'

urlpatterns = [
    path('classes/', views.classes_list, name='classes_list'),
    path('class/<int:class_id>/', views.class_view, name='class'),
    path('list/teachers/', views.teachers_view, name='teachers_list'),
    path('class/add/', views.add_class, name='add_class'),
    path('class/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('teachers/list/', views.teachers_view, name='teachers_list'),
    path('parents/', views.parents_view, name='parents_list'),
    path('academics/', views.academics_landing, name='academics_landing'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('subject/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('class-subject/add/', views.add_class_subject, name='add_class_subject'),
    path('class-subject/edit/<int:class_subject_id>/', views.edit_class_subject, name='edit_class_subject'),
]