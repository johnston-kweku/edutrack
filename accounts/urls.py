from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .reset import EduTrackPasswordResetConfirmView


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
    path('toggle/active/<int:user_id>/', views.toggle_active_state, name='toggle_active_state'),
    path('profile/', views.my_profile, name='my_profile'),
    path('user/profile/<int:user_id>/',  views.user_profile, name='user_profile'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='email_and_reset/password_reset.html',
             email_template_name='email_and_reset/password_reset_email.html',
             subject_template_name='email_and_reset/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='email_and_reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         EduTrackPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='email_and_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]