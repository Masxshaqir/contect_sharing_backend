

from .models import  Post,Comment, Vote
from rest_framework import serializers
from django.contrib.auth import get_user_model



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

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

class addVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
 

class UpdateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        partial = True