from django.contrib.auth import get_user_model

from rest_framework import serializers

from bson.objectid import ObjectId

from ..validators.datasets import (
    validate_dataset_name_type,
    validate_dataset_name_length
)
from ..db.collections import Dataset
from ..parsers.parser import ParsedDataset

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
    index_col = serializers.CharField(read_only=True)
    features = serializers.ListField(read_only=True)
    label = serializers.CharField(read_only=True)
    num_records = serializers.IntegerField(read_only=True)
    original_format = serializers.CharField(read_only=True)

    def __init__(self, instance=None, data=serializers.empty, *args, **kwargs):
        self.exclude_data = kwargs.pop('exclude_data', False)

        super().__init__(instance, data, *args, **kwargs)

        self.queryset = self._get_queryset()

    def _get_queryset(self):
        return Dataset.objects

    def to_representation(self, instance):
        representation = {}

        if hasattr(instance, 'uid') and instance.uid is not None:
            representation['uid'] = str(instance.uid)
        else:
            representation['uid'] = None

        if hasattr(instance, 'user_id') and instance.user_id is not None:
            representation['user_id'] = instance.user_id
        else:
            representation['user_id'] = None
        
        representation['name'] = instance.name

        if not self.exclude_data:
            representation['data'] = instance.data
            representation['index_col'] = getattr(instance, 'index_col', None)
            representation['features'] = getattr(instance, 'features', None)
            representation['label'] = getattr(instance, 'label', None)
            representation['num_records'] = getattr(
                instance, 'num_records', None)
            representation['original_format'] = getattr(
                instance, 'original_format', None)

        return representation
    
    def to_internal_value(self, data):
        parsed_data = data.get('data', None)

        data_is_parsed = False
        if parsed_data is not None and isinstance(parsed_data, ParsedDataset):
            data_is_parsed = True

        internal_val = {
            'user_id': data.get('user_id', None),
            'name': data.get('name', None),
            'data': parsed_data.get_data() if data_is_parsed else {}
        }

        uid = data.get('uid', None)
        if not isinstance(uid, ObjectId) and uid is not None:
            internal_val['uid'] = ObjectId(data['uid'])
        
        if data_is_parsed:
            internal_val['index_col'] = parsed_data.get_index_col()
            internal_val['features'] = parsed_data.get_features()
            internal_val['label'] = parsed_data.get_label()
            internal_val['num_records'] = parsed_data.get_num_records()
            internal_val['original_format'] = parsed_data.get_original_format()

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
