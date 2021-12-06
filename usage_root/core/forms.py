from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.conf import settings


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password1','password2')