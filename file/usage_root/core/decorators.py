from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('core:dashboard')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('core:dashboard')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Client Group':
			return redirect('core:client')

		elif group == 'App Admin Group':
			return view_func(request, *args, **kwargs)
		elif request.user.is_superuser:
			return redirect('admin/')
			# group,status = Group.objects.get_or_create(name = 'App Admin Group')
			# request.user.groups.add(group)
			# return view_func(request, *args, **kwargs)
   
	return wrapper_function

