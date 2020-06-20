from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bson import ObjectId
from bson.errors import InvalidId

from ..serializers.models import MLModelSerializer
from ..db.collections import MLModel


class Models(APIView):
    def get(self, request):
        by_fields = {'user_id': request.user.username}
        if 'dataset_id' in request.query_params:
            try:
                dataset_id = request.query_params['dataset_id']
                by_fields['dataset_id'] = ObjectId(dataset_id)
            except (TypeError, InvalidId):
                return Response(f'Invalid ID: {dataset_id}',
                                status=status.HTTP_400_BAD_REQUEST)

        models = MLModel.objects.get_all(by_fields, cast_into_cls=MLModel)
        serializer = MLModelSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class ModelDetail(APIView):
    def get_document(self, uid, user_id):
        model = MLModel.objects.get({'_id': uid, 'user_id': user_id})
        if model is None:
            raise Http404(f'No model found with ID {uid}')
        return model

    def get_object(self, uid, user_id):
        return MLModel.create(**self.get_document(ObjectId(uid), user_id))
    
    def get(self, request, uid):
        model = self.get_object(uid, request.user.username)
        return Response(status=status.HTTP_200_OK)
