from django.contrib.auth import get_user_model

from rest_framework import serializers

from bson.objectid import ObjectId

from ..validators.datasets import (
    validate_dataset_name_type,
    validate_dataset_name_length
)
from ..db.collections import Dataset

User = get_user_model()


class DatasetSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    name = serializers.CharField(required=True, validators=[
        validate_dataset_name_type,
        validate_dataset_name_length
    ])
    data = serializers.DictField(allow_empty=True, required=False)

    def __init__(self, instance=None, data=serializers.empty, *args, **kwargs):
        super().__init__(instance, data, *args, **kwargs)

        self.queryset = self._get_queryset()

    def _get_queryset(self):
        return Dataset.objects

    def to_representation(self, instance):
        representation = {}

        if instance.uid is not None:
            representation['uid'] = str(instance.uid)
        else:
            representation['uid'] = None

        representation['user_id'] = instance.user_id
        representation['name'] = instance.name
        representation['data'] = instance.data

        return representation
    
    def to_internal_value(self, data):
        internal_val = {'user_id': data.get('user_id', None),
                        'name': data.get('name', None),
                        'data': data.get('data', {})}

        uid = data.get('uid', None)
        if not isinstance(uid, ObjectId) and uid is not None:
            internal_val['uid'] = ObjectId(data['uid'])
        
        return internal_val

    def validate(self, data):
        if self.queryset.exists({'user_id': data['user_id'],
                                 'name': data['name']}):
            raise serializers.ValidationError(
                f'You already have a dataset called {data["name"]}'
            )
        return data
    
    def create(self):
        return Dataset.create(**self.validated_data)

    def save(self, dataset):
        if not isinstance(dataset, Dataset):
            raise TypeError('dataset must be of type Dataset')
        return self.queryset.save(dataset)
