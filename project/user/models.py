from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = models.BooleanField(default = False)
    MANAGER = models.BooleanField(default = False)
    WORKER = models.BooleanField(default = False)

    REQUIRED_FIELDS = ['ADMIN', 'MANAGER', 'WORKER', 'email']
