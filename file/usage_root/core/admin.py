from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import (
    Notification,
    Threshold,
    User,
    Bot,
    UserMessageData,
    ScrapedUser,
    Message,
    Text,
    RestrictedRoles,
    LogData
)
# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ('username','email','first_name','last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password','first_name','last_name','token')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username','email')
    ordering = ('username',)
    
admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_alive']
    list_filter = ['user', 'is_alive']
    search_fields = ['token']
    list_editable = ['is_alive']


@admin.register(UserMessageData)
class UserMessageDataAdmin(admin.ModelAdmin):
    list_filter = ['user']

@admin.register(ScrapedUser)
class ScrapedUserAdmin(admin.ModelAdmin):
    list_filter = ['texted', 'user']
    search_fields = ['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_filter = ['user']

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_filter = ['user']

@admin.register(RestrictedRoles)
class RoleAdmin(admin.ModelAdmin):
    list_filter = ['user']

@admin.register(LogData)
class LogDataAdmin(admin.ModelAdmin):
    list_filter = ['success', 'user']
    

@admin.register(Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ['value','flag']
    list_editable = ['flag']
admin.site.register(Notification)