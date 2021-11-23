from django.contrib.auth.signals import user_logged_in, user_logged_out,user_login_failed
from django.contrib.auth.models import User
from .models import *
from django.dispatch import receiver
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from django.core.signals import request_started, request_finished, got_request_exception

# @receiver(user_logged_in,sender=User)
def login_success(sender, request, user,**kwargs):
    print('logged in signal')
    print('sender',sender)
    print('request',request)
    print('user',user.email)
    print('kwargs',kwargs)
    
# user_logged_in.connect(login_success, sender=User)

# @receiver(user_logged_out,sender=User)
def logout_success(sender, request, user,**kwargs):
    print('logged out signal')
    print('sender',sender)
    print('request',request)
    print('user',user.email)
    print('kwargs',kwargs)
    
    
# @receiver(user_login_failed,sender=User)
def login_success(sender, credentials, request,**kwargs):
    print('login failed signal')
    print('sender',sender)
    print('credentials',credentials)
    print('request',request)
    print('kwargs',kwargs)
    
# @receiver(pre_save,sender=User)
def at_beginning_save(sender, instance,**kwargs):
    print('at_beginning_save')
    print('sender',sender)
    print('instance',instance)
    print('kwargs',kwargs)
    

# @receiver(post_save,sender=User)
def at_ending_save(sender, instance,created,**kwargs):
    if created:
        print('at_ending_save')
        print('sender',sender)
        print('instance',instance)
        print('created',created)
        print('kwargs',kwargs)
    else:
        print('elif')
        print('at_ending_save')
        print('sender',sender)
        print('instance',instance)
        print('created',created)
        print('kwargs',kwargs)
        
# @receiver(request_started)
def requset_started(sender, environ,**kwargs):
    print('request_started')
    print('sender',sender)
    print('environ',environ)
    print('kwargs',kwargs)
        
# @receiver(request_finished)
def requset_started(sender,**kwargs):
    print('request_finished')
    print('sender',sender)
    print('kwargs',kwargs)

# @receiver(got_request_exception)
def requset_started(sender,request,**kwargs):
    print('got_request_exception')
    print('sender',sender)
    print('request',request)
    print('kwargs',kwargs)