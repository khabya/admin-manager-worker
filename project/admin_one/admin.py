from django.contrib import admin
from .models import (
    Department,
    ManagerDepartment,
    WorkerManagerDepartment,
)

admin.site.register(Department)
admin.site.register(ManagerDepartment)
admin.site.register(WorkerManagerDepartment)