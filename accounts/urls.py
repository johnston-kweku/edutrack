from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('register/invalid/', views.invalid_invite, name='invalid_invite'),
    path('link/generate/', views.generate_invite_link, name='generate_invite_link'),
    path('user/delete/<str:username>/', views.delete_user, name='delete_user' ),
    path('logout/', views.logout_view, name='logout'),
    path('edit/profile/', views.edit_my_profile, name='edit_my_profile'),
]