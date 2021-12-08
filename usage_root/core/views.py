from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
# from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, admin_only ,allowed_users
from twilio.rest import Client
from django.conf import settings

from .forms import CustomUserCreationForm

from .models import (
    ScrapedUser,
    Bot,
    LogData,
    Threshold,
    User
)

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'core/index-admin.html', {
                'data': [
                    {
                        'name': str(user),
                        'bots_alive': Bot.objects.filter(user=user, is_alive=True).count(),
                        'users_scraped': ScrapedUser.objects.filter(user=user).count(),
                        'received_dm': LogData.objects.filter(user=user).count(),
                        'successful_dm': LogData.objects.filter(user=user, success=True).count(),
                        'unsuccessful_dm': LogData.objects.filter(user=user, success=False).count()
                    } for user in User.objects.all()
                ]   
            })
        else:
            user = request.user
            return render(request, 'core/index.html', {
                'bots_alive': Bot.objects.filter(user=user, is_alive=True).count(),
                'users_scraped': ScrapedUser.objects.filter(user=user).count(),
                'received_dm': LogData.objects.filter(user=user).count(),
                'successful_dm': LogData.objects.filter(user=user, success=True).count(),
                'unsuccessful_dm': LogData.objects.filter(user=user, success=False).count()
            })
    else:
        return redirect(reverse('core:login'))

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('core:index'))
    if request.method == 'GET':
        return render(request, 'core/login.html')

    token = request.POST.get('token')

    user = authenticate(request, token=token)


    if user is not None:
        login(request, user)
        return redirect(reverse('core:index'))
    else:
        return HttpResponse('Unauthorized', status=500)


def logout_view(request):
    logout(request)
    messages.info(request,'you have successfully logged out')
    return redirect(reverse('core:index'))


class SignupView(View):
    template_name = 'core/signup.html'
    @method_decorator(unauthenticated_user)
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        self.form = CustomUserCreationForm(request.POST)
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = request.POST['email']
            user = self.form.save()
            first_name = self.form.cleaned_data.get('first_name')
            group,status = Group.objects.get_or_create(name = 'Client Group')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + first_name)
            return redirect('core:login')
        else:
            messages.error(request,'please enter data correctly')
            self.first_name = request.POST.get('first_name')
            self.last_name = request.POST.get('last_name')
            self.email = request.POST.get('email')
            context = {
                "first_name": self.first_name,
                "last_name" : self.last_name,
                "email" : self.email
            }
            return render(request,self.template_name,context)
        
class LoginView(View):
    template_name = 'core/login1.html'
    @method_decorator(unauthenticated_user)
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        email = request.POST['email']
        password =request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None and user.groups.exists():
            auth_login(request,user)
            return redirect('core:dashboard')
        else:
            messages.error(request,'username or password incorrect')
            return redirect('core:login')
        
class CheckEmailView(View):
    def get(self, request):
        email = request.GET.get('email')
        if email:
            email_exists_condition = User.objects.filter(email__exact=email).exists()
        else:
            email_exists_condition = False
        data = {
        'email_exists':email_exists_condition,
        }
        return JsonResponse(data)
    

class DashboardView(View):
    template_name = 'core/dashboard-default.html'
    @method_decorator(login_required(login_url='core:login'))
    @method_decorator(admin_only)
    def get(self, request):
        client = Client(settings.ACCOUNT_API_KEY,settings.ACCOUNT_API_SECRET,settings.TWILIO_ACCOUNT_SID)
        # balance = float(client.api.v2010.balance.fetch().balance)
        balance = 35.5
        currency = client.api.v2010.balance.fetch().currency
        thresholds = Threshold.objects.all()
        if request.user.groups.all()[0].name == 'App Admin Group':
            group = True
        context = {
            'balance':balance,
            'thresholds':thresholds,
            'group':group
        }
        return render(request, self.template_name,context)
    
class ClientPageView(View):
    template_name = 'core/client-dashboard.html'
    @method_decorator(login_required(login_url='core:login'))
    @method_decorator(allowed_users(allowed_roles=['Client Group']))
    def get(self, request):
        return render(request, self.template_name)