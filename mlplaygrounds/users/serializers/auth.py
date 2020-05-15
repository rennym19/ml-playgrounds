from django.contrib.auth import authenticate, login, logout

from rest_framework import serializers

from mlplaygrounds.users.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=255)

    def __init__(self, data=serializers.empty, **kwargs):
        super().__init__(None, data, **kwargs)
        
        self.request = kwargs.get('request', None)
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
        super().init(instance=None, serializers.empty, **kwargs)

        self.request = kwargs.get('request', None)
        if self.request is None:
            raise serializers.ValidationError(
                'Request needed to log out.'
            )

    def save(self):
        return logout(self.request)
