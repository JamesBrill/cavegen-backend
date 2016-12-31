from django.db import models
from django.contrib.auth.models import User

class Cave(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, default=1)
