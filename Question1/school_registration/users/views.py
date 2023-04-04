from django.contrib.auth import get_user_model
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminUser
from .serializers import RegistrationSerializer, AuthTokenSerializer

User = get_user_model()


class RegisterUser(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("password2")

        user = User.objects.create_user(**serializer.validated_data)
        AuthToken.objects.create(user)
        return Response(
            {'success': 'User created successfully.'},
            status=status.HTTP_201_CREATED
        )


class Login(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
