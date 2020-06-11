from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .serializers import (
    TaskSerializer,
    ManagerWorkerTaskSerializer,
)
from manager.models import (
    Task,
    ManagerWorkerTask,
)

class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        task_serializer = TaskSerializer(data = request.data)
        if task_serializer.is_valid():
            task_serializer.save()

            return Response(task_serializer.data, status = status.HTTP_201_CREATED)

        return Response(task_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        task_list = Task.objects.all()
        task_serializer = TaskSerializer(task_list, mant = True)
        return Response(task_serializer.data, status = status.HTTP_200_OK)

class TaskChangeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        task_serializer = TaskSerializer(task, data = request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(task_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class ManagerWorkerTaskView(generics.ListCreateAPIView):
    queryset = ManagerWorkerTask.objects.all()
    serializer_class = ManagerWorkerTaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

class ManagerWorkerTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManagerWorkerTask.objects.all()
    serializer_class = ManagerWorkerTaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )