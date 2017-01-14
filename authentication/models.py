from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from urllib.parse import urlencode
from backend.utils import hash_email
from caves.models import Cave
import hashlib
import requests

class UserManager(models.Manager):
    def create(self, validated_data, profile=None):
        if profile is None:
            profile = {}

        validated_data['username'] = hash_email(validated_data['email'])
        user = self.model(**validated_data)
        user.save()
        userprofile = UserProfile(user=user, **profile)
        userprofile.save()

        return user

class UserProxy(User):
    objects = UserManager()

    def update(self, email, userprofile, first_name='', last_name=''):
        self.first_name = first_name
        self.last_name = last_name
        if 'access_token' in userprofile:
            self.userprofile.access_token = userprofile['access_token']
        if 'refresh_token' in userprofile:
            self.userprofile.refresh_token = userprofile['refresh_token']
        self.userprofile.picture = userprofile['picture']
        self.userprofile.display_name = userprofile['display_name']
        self.userprofile.save()
        self.save()
        return self

    class Meta:
        proxy = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.CharField(max_length=200, default='')
    display_name = models.CharField(max_length=50, default='anonymous')
    liked_caves = models.ManyToManyField(Cave)

    def __str__(self):
        return self.display_name
