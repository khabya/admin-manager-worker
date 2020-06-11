from django.db import models
from user.models import User 

class Department(models.Model):
    DEPARTMENT = models.CharField(max_length = 255)

    def __str__(self):
        return self.DEPARTMENT

class ManagerDepartment(models.Model):
    MANAGER = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'manager')
    DEPARTMENT = models.OneToOneField(Department, on_delete = models.CASCADE, \
        related_name = 'department')

    def __str__(self):
        return f"{self.DEPARTMENT} - {self.MANAGER}"

class WorkerManagerDepartment(models.Model):
    MANAGER_DEPARTMENT = models.ForeignKey(ManagerDepartment, on_delete = models.CASCADE, \
        related_name = 'manager_department')
    WORKER = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'worker')

    def __str__(self):
        return f"{self.MANAGER_DEPARTMENT} {self.WORKER}"
