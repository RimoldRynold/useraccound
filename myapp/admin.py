from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(UserProfile)
# admin.site.register(Posts)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','avatar','is_premium']
    
    
    
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id','userPost','title','body']
