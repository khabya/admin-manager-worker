from django.db import models
from admin_one.models import (
    WorkerManagerDepartment,
    Department,
)

class Task(models.Model):
    TASK_NAME = models.CharField(max_length = 255)
    TASK_DESCRIPTION = models.TextField()
    TASK_DEPARTMENT = models.ForeignKey(Department, on_delete = models.CASCADE, \
        related_name = 'task_department')

    def __str__(self):
        return f"{self.pk}"

def report_file(self, Filename):
    return "%s/%s/%s" % (str(self.WORKER), str(self.TASK), Filename)

class ManagerWorkerTask(models.Model):
    WORKER = models.ForeignKey(WorkerManagerDepartment, on_delete = models.CASCADE, \
        related_name = 'worker_task')
    TASK = models.ForeignKey(Task, on_delete = models.CASCADE, \
        related_name = 'task')
    REPORT = models.FileField(upload_to = report_file, blank = True)

    def __str__(self):
        return f"{self.WORKER} - {self.TASK}"



    


    


