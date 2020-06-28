from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = models.BooleanField(default = False)
    MANAGER = models.BooleanField(default = False)
    WORKER = models.BooleanField(default = False)

    REQUIRED_FIELDS = ['ADMIN', 'MANAGER', 'WORKER', 'email']

class UserLoginLogout(models.Model):
    USER = models.ForeignKey(User, related_name = 'user_login_logout', on_delete = models.CASCADE)
    DATE = models.DateField()
    LOGIN = models.TimeField()
    LOGOUT = models.TimeField(blank = True, null = True)

    def __str__(self):
        return f"{self.USER} - {self.DATE} => Login time {self.LOGIN}, Logout time {self.LOGOUT}"
