from django.urls import path, include
from . import views
from user.views import LoginView

urlpatterns = [
    path('registration/', views.UserRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('normal-login/', LoginView.as_view()),

    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]