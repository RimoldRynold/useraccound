from django.urls import path
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
    path('check_username/', CheckUserNameView.as_view(), name='check_username'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('maintenance',maintenance,name='maintenance')
]