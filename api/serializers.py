
from rest_framework import serializers
from myapp.models import *



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        # fields = ['id','title','body','created_at','changed_at']
        fields = '__all__'
        # exclude=('userPost',)
        