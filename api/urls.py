from django.urls import path, include

from myapp.views import PostUpdateView
from .views import *




urlpatterns = [
    path('',PostCreateAPIView.as_view()),
    path('<int:id>',PostUpdateAPIView.as_view()),
    
]