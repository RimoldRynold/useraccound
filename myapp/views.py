from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import * 
from django.contrib import messages
# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        posts = ''
    else:
        posts = Posts.objects.filter(userPost=request.user)
    return render(request,'home.html',{'user':request.user,'posts':posts})

def posts(request,pk):
    posts = Posts.objects.get(id=pk)
    return render(request,'posts.html',{'posts':posts})


def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():

            post_form.instance.userPost = request.user
            post_form.save()
            messages.success(request, 'Your post was successfully created!')
            return redirect('home')
        else:
            messages.error(request, 'Please enter correct data')
            return redirect('post_create')

    post_form = PostForm()
    return render(request, "create_post.html", context={"post_form": post_form})

def post_update(request,pk):
    if request.method == 'POST':
        post = Posts.objects.get(id=pk)
        post_form = PostForm(request.POST,instance=post)
        if post_form.is_valid():
            post_form.instance.userPost = request.user
            post_form.save()
            messages.success(request, 'Your post was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please enter correct data.')
            return redirect('post_update')
    else:
        post = Posts.objects.get(id=pk)
        post_form = PostForm(instance=post)
    return render(request, "update_post.html", context={"post_form": post_form})



def post_delete(request,pk):
    post = Posts.objects.get(id=pk)
    post.delete()
    return redirect('home')

def register(request):
    if request.method == 'POST':
    
        print(request.POST)
        print(request.FILES)
        form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            print('form valid')
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            messages.error(request,'please enter data correctly')
            return redirect('register')
     
    else:
        form = UserForm()
        profile_form = UserProfileForm()
    context = {
        'form':form,
        'profile_form':profile_form,
    }

    return render(request,'register.html',context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password =request.POST['password']
        print(password)
        
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password incorrect')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'you have successfully logged out')
    return redirect('login')

def accountSettings(request):
    logined_username = request.user
    user_obj = User.objects.get(username=logined_username)
    cust_obj = UserProfile.objects.get(user=user_obj)
    context = {
    'user':cust_obj
    }
    return render(request, 'account_settings.html', context)