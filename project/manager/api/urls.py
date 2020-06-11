from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.TaskView.as_view()),
    path('task/<pk>/', views.TaskChangeView.as_view()),
    path('manager-worker-task/', views.ManagerWorkerTaskView.as_view()),
    path('manager-worker-task/<pk>/', views.ManagerWorkerTaskDetailView.as_view()),
]