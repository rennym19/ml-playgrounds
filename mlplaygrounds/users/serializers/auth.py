from django.contrib.auth import authenticate, login, logout

from rest_framework import serializers

from mlplaygrounds.users.models import User
from mlplaygrounds.users.validators.password import (
    validate_is_alpha,
    validate_is_numeric,
    validate_not_short
)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def __init__(self, data=serializers.empty, **kwargs):
        super().__init__(None, data, **kwargs)
        
        self.request = self.context.get('request', None)
        if self.request is None:
            raise serializers.ValidationError(
                'Request needed to authenticate user.'
            )
        self.queryset = self._get_queryset()
    
    def _get_queryset(self):
        return User.objects

    def validate_username(self, username):
        if not self.queryset.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Could not find an user with username {username}'
            )
        return username

    def validate(self, data):
        user = self.queryset.get(username=data['username'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                f'Invalid password for user: {user.username}'
            )
        return data

    def save(self):
        return self.authenticate_user()

    def authenticate_user(self):
        user = authenticate(self.request,
                            username=self.validated_data['username'],
                            password=self.validated_data['password'])
        login(self.request, user)
        return user


class LogoutSerializer(serializers.Serializer):
    def __init__(self, **kwargs):
        super().__init__(None, serializers.empty, **kwargs)

        self.request = self.context.get('request', None)
        if self.request is None:
            raise serializers.ValidationError(
                'Request needed to log out.'
            )

    def save(self):
        return logout(self.request)


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(max_length=16, required=True)
    password = serializers.CharField(max_length=255,
                                     required=True,
                                     validators=[
                                         validate_is_alpha,
                                         validate_is_numeric,
                                         validate_not_short
                                     ])
    
    def __init__(self, data=serializers.empty, **kwargs):
        super().__init__(None, data, **kwargs)

        self.request = self.context.get('request', None)
        if self.request is None:
            raise serializers.ValidationError(
                'Request needed to log in user after registration.'
            )
        self.queryset = self._get_queryset()

    def _get_queryset(self):
        return User.objects

    def validate_username(self, username):
        if self.queryset.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Username {username} already in use.'
            )
        return username

    def validate_password(self, password):
        return password

    def validate_email(self, email):
        if self.queryset.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Email {email} already in use.'
            )
        return email

    def create(self, validated_data):
        return self.queryset.create_user(**validated_data)

    def login(self, user):
        login(self.request, user)
