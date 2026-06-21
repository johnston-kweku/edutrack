from django.urls import path
from . import views
app_name = 'academics'

urlpatterns = [
    path('classes/', views.classes_list, name='classes_list'),
    path('class/<int:class_id>/', views.class_view, name='class'),
    path('list/teachers/', views.teachers_view, name='teachers_list'),
    path('class/add/', views.add_class, name='add_class'),
    path('class/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('teachers/list/', views.teachers_view, name='teachers_list')
]