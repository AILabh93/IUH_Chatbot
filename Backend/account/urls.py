from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create-user/', views.createUser),
    path('login/', views.logIn),
    path('update/', views.updateUser),
    path('check-login/', views.chech_login),
    path('get-all/', views.getAllUser),
    path('get-user-id/', views.getUserByID),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             subject_template_name='password_reset_subject.txt',
             email_template_name='password_reset_email.html',
         ), name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_mail_sent.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirmation.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_completed.html'
         ), name='password_reset_complete')
]
