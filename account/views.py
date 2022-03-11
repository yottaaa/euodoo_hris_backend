from urllib import response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from knox.views import LoginView as KnoxLoginView

from account.serializers import UserSerializer

def register(request):
    pass

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data['user'] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class AdminLoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data['user'] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.is_superuser:
            login(request, user)
        else: 
            return Response({"detail":"Not admin"},status=status.HTTP_401_UNAUTHORIZED)
        return super(AdminLoginAPI, self).post(request, format=None)