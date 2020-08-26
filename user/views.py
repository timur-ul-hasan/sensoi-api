from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from django.contrib.auth.models import Permission, Group
from rest_framework import permissions
from rest_framework.response import Response

from .models import (
    User
)

from django.conf import settings


from .serializers import (
    RegisterUserSerializer,
    TokenObtainPairWithUserDataSerializer,
    EmailTokenObtainPairWithUserDataSerializer,
    UsernameTokenObtainPairWithUserDataSerializer,
)

def register_user(request):
    user = None
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.is_active = True
        user.save()

    return user


class RegisterUser(GenericAPIView):
    permission_classes = ()
    serializer_class = RegisterUserSerializer

    def get_queryset(self):
        return None

    def post(self, request):
        if settings.ENABLE_USER_REGISTRATION:
            user = register_user(request=request)
            refresh = RefreshToken.for_user(user)

            return Response({
                "message":
                "user created with id %s, please check your email %s to verify your registration"
                % (user.id, user.email),
                "id": user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"message": "Registration has been disabled"})

class EmailTokenObtainPairWithUserDataView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    em: email or username

    """

    serializer_class = EmailTokenObtainPairWithUserDataSerializer


class UsernameTokenObtainPairWithUserDataView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    email: test@test.com
    password: some_password

    """

    serializer_class = UsernameTokenObtainPairWithUserDataSerializer