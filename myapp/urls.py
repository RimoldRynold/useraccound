from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('register',RegisterView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',logoutUser,name='logout'),
    path('account', AccountSettingsView.as_view(), name='account'),
    path('posts/<str:pk>',PostView.as_view(),name='posts'),
    path('post_create',PostCreateView.as_view(),name='post_create'),
    path('post_update/<str:pk>',PostUpdateView.as_view(),name='post_update'),
    path('post_delete/<str:pk>',DeletePostView.as_view(),name='post_delete'),
    path('check-username-email/', CheckUserNameEmailView.as_view(), name='check_username'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('maintenance',MaintenanceView.as_view(),name='maintenance'),



    path('reset_password',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='reset_password'),

    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),

    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),
]
