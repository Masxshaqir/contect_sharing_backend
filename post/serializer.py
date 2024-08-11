

from .models import  Post,Comment
from rest_framework import serializers
from django.contrib.auth import get_user_model



class addPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
 

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        partial = True
        

class addCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
 

class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        partial = True