from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user_id', 'picture', 'display_name', 'liked_caves')

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'userprofile')
        extra_kwargs = {
            'userprofile': {'write_only': True}
        }
