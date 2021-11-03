from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('logout',logoutUser,name='logout'),
    path('posts/<str:pk>',posts,name='posts')
    # path('post_create',post_create,name='post_create')
]