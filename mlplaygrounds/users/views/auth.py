from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mlplaygrounds.users.models import User
from mlplaygrounds.users.serializers.users import UserSerializer
from mlplaygrounds.users.serializers.auth import (
    LoginSerializer,
    RegisterSerializer
)


class Login(APIView):
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'Already logged in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user, token = serializer.save()
            if user is not None:
                return Response({'user': UserSerializer(user).data,
                                 'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'Log out before registering a new user'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data,
                                        context={'request': request})
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            if user is not None:
                token = serializer.login(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
