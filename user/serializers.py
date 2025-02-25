from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User 
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.models import Permission, Group
from django_middleware_global_request.middleware import get_request
from Util.alfresco import createPerson


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    full_name = serializers.CharField(max_length=254)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)
    # serviceprovider = RegisterServiceProviderSerializer(required=False)

    # def validate(self, data):
    #     """
    #     Check that start is before finish.
    #     """
    #     if data["user_type"] is "service_provider" and 'serviceprovider' not in data:
    #         raise serializers.ValidationError(
    #             "Service provider is required for Service Provider Registration."
    #         )
    #     return data

    def update(self, instance, validated_data):
        raise PermissionDenied(detail="You can't update user registration")

    def create(self, validated_data):

        if self.validated_data['password1'] != self.validated_data['password2']:
            raise ValidationError(
                detail="password1 and password2 does not match")

        password_validation.validate_password(
            password=self.validated_data['password1'],
            password_validators=password_validation.
            get_default_password_validators())

        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password1'],
                full_name=validated_data['full_name'],
               )
            createPerson(user)
            return user
        except IntegrityError:
            raise ValidationError("Can't create user with this combination")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',
                  'user_type')


class TokenObtainPairWithUserDataSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields[self.username_field]

    @staticmethod
    def get_groups(obj):
        data = {}
        for group in obj.groups.all():
            perms = group.permissions.values('codename')
            data[group.name] = [entry['codename'] for entry in perms]
        return data

    @classmethod
    def get_token(cls, user):
        request = get_request()
        token = super().get_token(user)
        token['superuser'] = user.is_superuser
        token['groups'] = TokenObtainPairWithUserDataSerializer.get_groups(
            user)
        return token


class EmailTokenObtainPairWithUserDataSerializer(
        TokenObtainPairWithUserDataSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = 'email'
        self.fields[self.username_field] = serializers.CharField()


class UsernameTokenObtainPairWithUserDataSerializer(
        TokenObtainPairWithUserDataSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = 'username'
        self.fields[self.username_field] = serializers.CharField()