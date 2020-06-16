from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status

from bson import ObjectId

from ..serializers.datasets import DatasetSerializer
from ..parsers.parser import DatasetParser
from ..parsers.exceptions import (InvalidFormat, InvalidFile, InvalidFeature)
from ..db.collections import Dataset


class Datasets(APIView):
    def get(self, request):
        datasets = Dataset.objects.get_all({'user_id': request.user.username},
                                           cast_into_cls=Dataset)
        serializer = DatasetSerializer(datasets, many=True, exclude_data=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_data = {'user_id': request.user.username}
        serializer = DatasetSerializer(data={**request.data, **user_data})
        
        if serializer.is_valid():
            dataset = serializer.create()
            dataset = serializer.save(dataset)
            return Response(DatasetSerializer(dataset).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetDetail(APIView):
    def get_document(self, uid, user_id):
        document = Dataset.objects.get({'user_id': user_id, '_id': uid})
        if document is None:
            raise Http404(f'No dataset found with ID {uid}')
        return document

    def get_object(self, uid, user_id):
        return Dataset.create(**self.get_document(ObjectId(uid), user_id))

    def get(self, request, uid):
        dataset = self.get_object(uid, request.user.username)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, uid):
        dataset = self.get_object(uid, request.user.username)

        serializer = DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            dataset = serializer.update()
            return Response(DatasetSerializer(dataset).data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        deleted = Dataset.objects.delete({'user_id': request.user.username,
                                          '_id': uid})
        if not deleted:
            raise Http404(
                f'Could not find a dataset of id {uid} for your user')
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def parse_dataset(request):
    label = request.data.get('label', None)
    parser = DatasetParser(request.data.get('data', None),
                           file_format='csv',
                           to_format='json',
                           label=label if label != '' else None,
                           problem_type=request.data.get('problem_type', None))

    try:
        parsed_dataset = parser.parse()
    except (InvalidFormat, InvalidFile, InvalidFeature) as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = DatasetSerializer(data={
        'name': request.data.get('name', None),
        'data': parsed_dataset,
        'user_id': request.user.username,
        'problem_type': request.data.get('problem_type', None)
    })

    if serializer.is_valid():
        dataset = serializer.create()
        dataset = serializer.save(dataset)
        return Response(DatasetSerializer(dataset).data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
