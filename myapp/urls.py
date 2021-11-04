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
    path('post_delete/<str:pk>',post_delete,name='post_delete')
]