from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    DepartmentSerializer,
    ManagerDepartmentSerializer,
    WorkerManagerDepartmentSerializer,
    UserDetailSerializer,
)

from admin_one.models import (
    Department,
    ManagerDepartment,
    WorkerManagerDepartment,
)
from user.models import User 

def getting_context(status, success, message, data):
    context = {}
    context['status']   = status
    context['success']  = success
    context['message']  = message
    context['data']     = data

    return context

class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        department_serializer = DepartmentSerializer(data = request.data)
        if department_serializer.is_valid():
            department_serializer.save()

            context = getting_context(status.HTTP_201_CREATED, True, f"The new department added successfully", \
                department_serializer.data)
            return Response(context, status = status.HTTP_201_CREATED)
        
        context = getting_context(status.HTTP_400_BAD_REQUEST, False, f"Unable to create new department", \
            department_serializer.errors)
        return Response(context, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)
        
        info = {}
        department_list = Department.objects.all()
        department_serializer = DepartmentSerializer(department_list, many = True)

        info['department-list'] = department_serializer.data
        context = getting_context(status.HTTP_200_OK, True, f"List of all available department", \
            info)
        return Response(context, status = status.HTTP_200_OK)

class DepartmentChangeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def put(self, request, pk):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        try:
            department = Department.objects.get(pk = pk)
        except Department.DoesNotExist:
            context = getting_context(status.HTTP_404_NOT_FOUND, False, f"Unable to find the particular department", \
                [])
            return Response(context, status = status.HTTP_404_NOT_FOUND)
        
        department_serializer = DepartmentSerializer(department, data = request.data)
        if department_serializer.is_valid():
            department_serializer.save()

            context = getting_context(status.HTTP_202_ACCEPTED, True, f"The department updated successful", \
                department_serializer.data)
            return Response(context, status = status.HTTP_202_ACCEPTED)
        
        context = getting_context(status.HTTP_400_BAD_REQUEST, False, f"Unable to update the department",\
            department_serializer.errors)
        return Response(context, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        try:
            department = Department.objects.get(pk = pk)
        except Department.DoesNotExist:
            context = getting_context(status.HTTP_404_NOT_FOUND, False, f"Unable to find the particular department", \
                [])
            return Response(context, status = status.HTTP_404_NOT_FOUND)

        department.delete()
        
        context = getting_context(status.HTTP_204_NO_CONTENT, True, f"Successful deleted department", \
            [])
        return Response(context, status = status.HTTP_204_NO_CONTENT)
        
class ManagerList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant fetch all managers data", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)
    
        info = {}
        manager_list = User.objects.filter(MANAGER = True)
        manager_serializer = UserDetailSerializer(manager_list, many = True)

        info['manager-list'] = manager_serializer.data
        context = getting_context(status.HTTP_200_OK, True, f"List of all managers", \
            info)
        return Response(context, status = status.HTTP_200_OK)

class WorkerList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant fetch all workers data", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)
    
        info = {}
        worker_list = User.objects.filter(WORKER = True)
        worker_serializer = UserDetailSerializer(worker_list, many = True)

        info['manager-list'] = worker_serializer.data
        context = getting_context(status.HTTP_200_OK, True, f"List of all workers", \
            info)
        return Response(context, status = status.HTTP_200_OK)

class ManagerDepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant allot manager to department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        manager_department_serializer = ManagerDepartmentSerializer(data = request.data)
        if manager_department_serializer.is_valid():
            manager_department_serializer.save()

            context = getting_context(status.HTTP_201_CREATED, True, f"Alloted manager to department", \
                manager_department_serializer.data)
            return Response(context, status = status.HTTP_201_CREATED)
        
        context = getting_context(status.HTTP_400_BAD_REQUEST, False, f"Unable to allot", \
            manager_department_serializer.errors)
        return Response(context, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        info = {}
        manager_department_list = ManagerDepartment.objects.all()
        manager_department_serializer = ManagerDepartmentSerializer(manager_department_list, many = True)

        info['manager-department'] = manager_department_serializer.data
        context = getting_context(status.HTTP_200_OK, True, f"Fetching all department with managers", \
            info)
        return Response(context, status = status.HTTP_200_OK)

class WorkerManagerDepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant allot worker to department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        worker_manager_department_serializer = WorkerManagerDepartmentSerializer(data = request.data)
        if worker_manager_department_serializer.is_valid():
            worker_manager_department_serializer.save()

            context = getting_context(status.HTTP_201_CREATED, True, f"Alloted worker to this department", \
                worker_manager_department_serializer.data)
            return Response(context, status = status.HTTP_201_CREATED)
        context = getting_context(status.HTTP_400_BAD_REQUEST, False, f"Unable to allot worker to department", \
            worker_manager_department_serializer.errors)
        return Response(context, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant allot worker to department", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        info = {}
        worker_manager_department_list = WorkerManagerDepartment.objects.all()
        worker_manager_department_serializer = WorkerManagerDepartmentSerializer(worker_manager_department_list, many = True)

        info['worker-manager-department'] = worker_manager_department_serializer.data
        context = getting_context(status.HTTP_200_OK, True, f"Fetching all department with manager and workers", \
            info)
        return Response(context, status = status.HTTP_200_OK)