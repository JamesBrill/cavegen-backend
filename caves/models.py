import uuid
from django.db import models
from django.contrib.auth.models import User

class Cave(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey(User, default=1)
