from rest_framework import serializers
from manager.models import (
    Task,
    ManagerWorkerTask,
)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['TASK_NAME', 'TASK_DESCRIPTION', 'TASK_DEPARTMENT']

class ManagerWorkerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerWorkerTask
        fields = ['WORKER', 'TASK', 'REPORT']