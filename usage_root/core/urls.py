from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path('index', index, name='index'),
    path('temp_login', login_view, name='login_view'),
    path('logout', logout_view, name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('login', LoginView.as_view(), name='login'),
    path('admin-dashboard', DashboardView.as_view(), name='dashboard'),
    path('', ClientPageView.as_view(), name='client'),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
