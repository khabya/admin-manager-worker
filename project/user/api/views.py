from django.conf import settings

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from allauth.account import app_settings as allauth_settings

from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_auth.app_settings import (
    TokenSerializer,
    JWTSerializer,
)

from user.models import User 

def getting_context(status, success, message, data):
    context = {}
    context['status']   = status
    context['success']  = success
    context['message']  = message
    context['data']     = data

    return context

class UserRegisterView(RegisterView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        if self.request.user.ADMIN == False:
            context = getting_context(status.HTTP_401_UNAUTHORIZED, False, f"This user cant add new user", \
                [])
            return Response(context, status = status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        context = getting_context(status.HTTP_201_CREATED, True, f'User created successful', \
            self.get_response_data(user))

        return Response(context, status=status.HTTP_201_CREATED, headers=headers)

class UserLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})
        
        context = getting_context(status.HTTP_200_OK, True, f"Getting the token of the logged in user", \
            serializer.data)

        response = Response(context, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response
