from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import * 
from .models import *
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.


class HomeView(View):
    template_name = 'home.html'
    def get(self, request):
        if not request.user.is_authenticated:
            posts = ''
        else:
            posts = Posts.objects.filter(userPost=request.user)
        return render(request,self.template_name,{'user':request.user,'posts':posts})


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
            messages.info(request,'you have successfully logged in')
            return redirect('home')
        else:
            messages.info(request,'username or password incorrect')
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
        cust_obj = UserProfile.objects.get(user=user_obj)
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


def maintenance(request):
    return render(request,'maintenance.html')