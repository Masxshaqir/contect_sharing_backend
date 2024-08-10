

from .models import Friend
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class updateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        partial = True
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password','first_name','last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class addFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'