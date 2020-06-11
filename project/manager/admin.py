from django.contrib import admin
from .models import (
    Task,
    ManagerWorkerTask,
)

admin.site.register(Task)
admin.site.register(ManagerWorkerTask)