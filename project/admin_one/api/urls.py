from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.ManagerList.as_view()),
    path('worker/', views.WorkerList.as_view()),
    path('department/', views.DepartmentView.as_view()),
    path('department/<pk>/', views.DepartmentChangeView.as_view()),
    path('manager-department/', views.ManagerDepartmentView.as_view()),
    path('worker-manager-department/', views.WorkerManagerDepartmentView.as_view()),
]