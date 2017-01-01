import uuid
from django.db import models
from django.contrib.auth.models import User

class Cave(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=256, null=True)
    text = models.TextField()
    author = models.ForeignKey(User, default=1)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Untitled'
        super(Cave, self).save(*args, **kwargs)
