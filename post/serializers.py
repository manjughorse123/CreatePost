from rest_framework import serializers
from django.contrib.auth.models import User
from  .models import *



class UserLoginSerializer(serializers.ModelSerializer):
   
    class Meta:
       model = User
       fields = ('id','username','email',)


class PostSerializer(serializers.ModelSerializer):
   

    class Meta:
       model = Post
       fields = "__all__"
       
class PostListSerializer(serializers.ModelSerializer):
   

    class Meta:
       model = Post
       fields = "__all__"
       
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = UserLoginSerializer(instance.author).data

        return response

   