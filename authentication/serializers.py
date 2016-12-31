from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'userprofile')
        extra_kwargs = {
            'userprofile': {'write_only': True}
        }
