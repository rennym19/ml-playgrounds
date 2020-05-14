from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from mlplaygrounds.users.serializers.users import UserSerializer


@api_view(['GET'])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
