from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import User


UserModel = get_user_model()


class LoginBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        token = kwargs.get('token')
        if token:
            try:
                user = User.objects.get(token=token).user
                return user
            except:
                return None
        else:
            try:
                user = UserModel.objects.get(
                    Q(email__exact=email))
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            except MultipleObjectsReturned:
                return User.objects.filter(mobile=email).order_by('id').first()
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None