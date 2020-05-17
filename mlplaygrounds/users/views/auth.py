from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mlplaygrounds.users.models import User
from mlplaygrounds.users.serializers.auth import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer
)


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'Already logged in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user is not None:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You\'re not logged in.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = LogoutSerializer(context={'request': request})
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'Log out before registering a new user'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data,
                                        context={'request': request})
        if serializer.is_valid():
            new_user = serializer.create(serializer.validated_data)
            if new_user is not None:
                serializer.login(new_user)
                return Response(serializer.validated_data,
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
