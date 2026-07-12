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
    path('academics/', views.academics_hub, name='academics_hub'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('subject/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('class-subject/add/', views.add_class_subject, name='add_class_subject'),
    path('class-subject/edit/<int:class_subject_id>/', views.edit_class_subject, name='edit_class_subject'),
    path('academic-years/add/', views.add_academic_year, name='add_academic_year'),
    path('academic-years/<int:pk>/edit/', views.edit_academic_year, name='edit_academic_year'),
    path('terms/add/', views.add_term, name='add_term'),
    path('terms/<int:pk>/edit/', views.edit_term, name='edit_term'),
    path('assessment/create/', views.add_assessment, name='add_assessment'),
    path('record/assessment/<int:assessment_id>/', views.record_class_assessment, name='record_class_assessment'),
]