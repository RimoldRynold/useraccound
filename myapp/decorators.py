from django.contrib.auth import decorators
from .models import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# def is_premium_user(view_func):
#     def wrapper_func(request, *args ,**kwargs):
#         print('requset',UserProfile.objects.get())
#         if request.user.is_superuser:
           
#             return view_func(request, *args ,**kwargs)
#         else:
#             raise PermissionDenied
#     return wrapper_func


def is_premium_user(view_func):
    def wrapper_func(request, *args ,**kwargs):
     
        if UserProfile.objects.filter(is_premium=True):
            # raise PermissionDenied
            if not request.user.is_authenticated:
                post = ''
            else:
                post = Posts.objects.all()
            paginator = Paginator(post, 5)
            page = request.GET.get('page', 1)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            return render(request,'home.html',{'user':request.user,'posts':posts})
        else:
            return view_func(request, *args ,**kwargs)
    return wrapper_func