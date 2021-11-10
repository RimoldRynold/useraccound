from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save,pre_save,post_delete
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string



# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to ='uploads/')
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            img = self.avatar.url
        except:
            img = ''
        return img

class Posts(models.Model):
    userPost = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# def save_post(sender, instance, **kwargs):
#     print('post created')

# def after_delete_post(sender, instance, **kwargs):
#     print('post deleted')

# pre_save.connect(save_post, sender=Posts)
# post_save.connect(save_post, sender=Posts)
# post_delete.connect(after_delete_post,sender=Posts)

# def success(sender, instance, **kwargs):
#     if UserProfile.objects.filter(user__email__exact=instance.user.email).exists():
#         print('if uerprofile')
#     else:
#         print('else uerprofile')
#         print('instance',instance.user.email)
#         template = render_to_string('email.html',{'name':instance.user})
#         email = EmailMessage(
#             'Thanks for registering',
#             template,
#             settings.EMAIL_HOST_USER,
#             [instance.user.email],
#         )
#         email.fail_silently=False
#         email.send()

# post_save.connect(success, sender=UserProfile)

def success(sender, instance, **kwargs):
    if User.objects.filter(email__exact=instance.email).exists():
        print('if user')
    else:
        print('else user')
        template = render_to_string('email.html',{'name':instance})
        email = EmailMessage(
            'Thanks for registering',
            template,
            settings.EMAIL_HOST_USER,
            [instance.email],
        )
        email.fail_silently=False
        email.send()

pre_save.connect(success, sender=User)