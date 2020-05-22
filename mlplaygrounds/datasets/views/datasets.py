from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..db.connection import MongoAccessObject 


class Datasets(APIView):
    def post(self, request):
        data_bank = MongoAccessObject()
        data_bank.insert(request.user.username, request.data)
        return Response('Done. Check DB.')
