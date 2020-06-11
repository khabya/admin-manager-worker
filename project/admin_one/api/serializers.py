from rest_framework import serializers
from admin_one.models import (
    Department,
    ManagerDepartment,
    WorkerManagerDepartment,
)
from user.models import User 

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['pk', 'DEPARTMENT']

class ManagerDepartmentSerializer(serializers.ModelSerializer):
    manager = serializers.SerializerMethodField('get_manager')
    department = serializers.SerializerMethodField('get_department')

    class Meta:
        model = ManagerDepartment
        fields = ['MANAGER', 'manager', 'DEPARTMENT', 'department']

    def get_department(self, obj):
        department = obj.DEPARTMENT.DEPARTMENT
        return department

    def get_manager(self, obj):
        manager = obj.MANAGER.username
        return manager
        
class WorkerManagerDepartmentSerializer(serializers.ModelSerializer):
    manager = serializers.SerializerMethodField('get_manager')
    department = serializers.SerializerMethodField('get_department')
    worker = serializers.SerializerMethodField('get_worker')

    class Meta:
        model = WorkerManagerDepartment
        fields = ['MANAGER_DEPARTMENT', 'WORKER', 'manager', 'department', 'worker']

    def get_manager(self, obj):
        manager = obj.MANAGER_DEPARTMENT.MANAGER.username
        return manager

    def get_department(self, obj):
        department = obj.MANAGER_DEPARTMENT.DEPARTMENT.DEPARTMENT
        return department

    
    def get_worker(self, obj):
        worker = obj.WORKER.username
        return worker

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'WORKER', 'MANAGER', 'ADMIN']