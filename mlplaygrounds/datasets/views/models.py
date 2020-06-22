from django.http import Http404
from django.core.exceptions import SuspiciousOperation

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
        serializer = MLModelSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.create()
            model = serializer.save(model)
            return Response(MLModelSerializer(model).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelDetail(APIView):
    def get_document(self, uid, user_id):
        model = MLModel.objects.get({'_id': uid, 'user_id': user_id})
        if model is None:
            raise Http404(f'No model found with ID {uid}')
        return model

    def get_object(self, uid, user_id):
        try:
            return MLModel.create(**self.get_document(ObjectId(uid), user_id))
        except (TypeError, InvalidId):
            raise SuspiciousOperation('Invalid ID')
    
    def get(self, request, uid):
        model = self.get_object(uid, request.user.username)
        serializer = MLModelSerializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, uid):
        model = self.get_object(uid, request.user.username)

        serializer = MLModelSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            model = serializer.update(model, serializer.validated_data)
            return Response(MLModelSerializer(model).data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        model = self.get_object(uid, request.user.username)
        deleted = MLModel.objects.delete({'_id': model.uid,
                                          'user_id': model.user_id})
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Error while deleting model',
                        status=status.HTTP_400_BAD_REQUEST)
