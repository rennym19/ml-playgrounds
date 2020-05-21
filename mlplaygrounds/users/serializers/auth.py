from django.contrib.auth import authenticate

from rest_framework import serializers

from knox.models import AuthToken

from mlplaygrounds.users.models import User
from mlplaygrounds.users.serializers.users import UserSerializer
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
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user is None:
            raise serializers.ValidationError(
                f'Invalid password for user: {data["username"]}'
            )
        return data

    def save(self):
        user = User.objects.get(username=self.validated_data['username']) 
        _, token = AuthToken.objects.create(user=user)
        return user, token 


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

        self.queryset = self._get_queryset()

    def _get_queryset(self):
        return User.objects

    def validate_username(self, username):
        if self.queryset.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Username {username} already in use.'
            )
        return username

    def validate_email(self, email):
        if self.queryset.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Email {email} already in use.'
            )
        return email

    def create(self, validated_data):
        return self.queryset.create_user(**validated_data)

    def login(self, user):
        _, token = AuthToken.objects.create(user=user)
        return token
