from django.db.models.signals import pre_delete
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .forms import * 
from .models import *
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse
from .decorators import *
# Create your views here.


class HomeView(View):
    template_name = 'home.html'
    @method_decorator(is_premium_user)
    def get(self, request):
        if not request.user.is_authenticated:
            post = ''
        else:
            post = Posts.objects.filter(userPost=request.user)
        paginator = Paginator(post, 5)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request,self.template_name,{'user':request.user,'posts':posts})

# @receiver(request_finished)
# def post_request_receiver(sender, **kwargs):
#     print('request finished')


class PostView(View):
    template_name = 'posts.html'
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        posts = Posts.objects.get(id=pk)
        return render(request,self.template_name,{'posts':posts})


class PostCreateView(View):
    template_name = 'create_post.html'
    form_class= PostForm
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        post_form = self.form_class()
        return render(request, self.template_name, context={"post_form": post_form})
    def post(self,request):
        post_form = self.form_class(request.POST)
        if post_form.is_valid():
            post_form.instance.userPost = request.user
            post_form.save()
            messages.success(request, 'Your post was successfully created!')
            return redirect('home')
        else:
            messages.error(request, 'Please enter correct data')
            return redirect('post_create')


class PostUpdateView(View):
    template_name = "update_post.html"
    form_class = PostForm
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        post = Posts.objects.get(id=pk)
        post_form = self.form_class(instance=post)
        return render(request, self.template_name, context={"post_form": post_form})
    def post(self, request, pk):
        post = Posts.objects.get(id=pk)
        post_form = self.form_class(request.POST,instance=post)
        if post_form.is_valid():
            post_form.instance.userPost = request.user
            post_form.save()
            messages.success(request, 'Your post was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please enter correct data.')
            return redirect('post_update')


class DeletePostView(View):
    @method_decorator(login_required(login_url='login'))
    def post(self,request,pk):
        post = Posts.objects.get(id=pk).delete()
        messages.info(request,'Post deleted successfully!')
        return redirect('home')

class RegisterView(View):
    template_name = 'register.html'
    def get(self, request):
        self.form = UserForm()
        self.profile_form = UserProfileForm()
        context = {
        'form':self.form,
        'profile_form':self.profile_form,
         }
        return render(request,self.template_name,context)
    def post(self,request):
        self.form = UserForm(request.POST)
        self.profile_form = UserProfileForm(request.POST,request.FILES)
        if self.form.is_valid() and self.profile_form.is_valid():
         
            user = self.form.save()
            profile = self.profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = self.form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            messages.error(request,'please enter data correctly')
            return redirect('register')

class LoginView(View):
    template_name = 'login.html'
    def get(self,request):
        print('path info',request.META['PATH_INFO'])
        return render(request,self.template_name)
    def post(self,request):
        username = request.POST['username']
        password =request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            messages.success(request,'you have successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'username or password incorrect')
            return redirect('login')


def logoutUser(request):
    logout(request)
    messages.info(request,'you have successfully logged out')
    return redirect('login')


class AccountSettingsView(View):
    template_name = 'account_settings.html'
    @method_decorator(login_required(login_url='login'))
    
    def get(self,request):
        logined_username = request.user
        user_obj = User.objects.get(username=logined_username)
        if UserProfile.objects.filter(user__username=logined_username).exists():
            cust_obj = UserProfile.objects.get(user=user_obj)
        else:
            cust_obj = ''
        context = {
        'user':cust_obj
        }
        return render(request, self.template_name, context)


class CheckUserNameView(View):
    def get(self, request):
        username = request.GET.get('username')
        email = request.GET.get('email')
        data = {
        'username_exists':UserProfile.objects.filter(user__username__iexact=username).exists(),
        }
        return JsonResponse(data)


class CheckEmailView(View):
    def get(self, request):
        email = request.GET.get('email')
        data = {
        'email_exists':UserProfile.objects.filter(user__email__iexact=email).exists(),
        }
        return JsonResponse(data)


class MaintenanceView(View):
    template_name = 'maintenance.html'
    def get(self,request):
        return render(request,self.template_name)



