from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('logout',logoutUser,name='logout'),
    path('account', accountSettings, name='account'),
    path('posts/<str:pk>',posts,name='posts'),
    path('post_create',post_create,name='post_create'),
    path('post_update/<str:pk>',post_update,name='post_update'),
    path('post_delete/<str:pk>',DeletePostView.as_view(),name='post_delete'),
    path('check_username/', check_username, name='check_username'),
    path('check_email/', check_email, name='check_email'),
]