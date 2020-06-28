from django.contrib import admin
from .models import User, UserLoginLogout

admin.site.register(User)
admin.site.register(UserLoginLogout)
