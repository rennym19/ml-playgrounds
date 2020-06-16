from django.contrib.auth import get_user_model

from rest_framework import serializers

from bson.objectid import ObjectId

from ..validators.datasets import (
    validate_dataset_name_type,
    validate_dataset_name_length,
    validate_problem_type
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
    problem_type = serializers.CharField(required=True)
    data = serializers.DictField(allow_empty=True, required=False)
    index_col = serializers.CharField(read_only=True)
    features = serializers.ListField(read_only=True)
    label = serializers.CharField(read_only=True)
    label_data = serializers.ListField(read_only=True)
    num_records = serializers.IntegerField(read_only=True)
    original_format = serializers.CharField(read_only=True)
    not_assigned_pct = serializers.FloatField(read_only=True)
    y_value_counts = serializers.ListField(read_only=True)

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

        if hasattr(instance, 'user_id'):
            representation['user_id'] = instance.user_id
        else:
            representation['user_id'] = None

        if hasattr(instance, 'problem_type'):
            representation['problem_type'] = instance.problem_type
        else:
            representation['problem_type'] = None
        
        representation['name'] = instance.name

        if not self.exclude_data:
            representation['data'] = instance.data
            representation['index_col'] = getattr(instance, 'index_col', None)
            representation['features'] = getattr(instance, 'features', None)
            representation['label'] = getattr(instance, 'label', None)
            representation['label_data'] = getattr(
                instance, 'label_data', None)
            representation['num_records'] = getattr(
                instance, 'num_records', None)
            representation['original_format'] = getattr(
                instance, 'original_format', None)
            representation['not_assigned_pct'] = getattr(
                instance, 'not_assigned_pct', None)
            representation['y_value_counts'] = getattr(
                instance, 'y_value_counts', None)

        return representation
    
    def to_internal_value(self, data):
        parsed_data = data.get('data', None)

        data_is_parsed = False
        if parsed_data is not None and isinstance(parsed_data, ParsedDataset):
            data_is_parsed = True

        internal_val = {
            'user_id': data.get('user_id', None),
            'name': data.get('name', None),
            'data': parsed_data.get_data() if data_is_parsed else {},
            'problem_type': data.get('problem_type')
        }

        uid = data.get('uid', None)
        if not isinstance(uid, ObjectId) and uid is not None:
            internal_val['uid'] = ObjectId(data['uid'])
        
        if data_is_parsed:
            internal_val['index_col'] = parsed_data.get_index_col()
            internal_val['features'] = parsed_data.get_features()
            internal_val['label'] = parsed_data.get_label()
            internal_val['label_data'] = parsed_data.get_label_data()
            internal_val['num_records'] = parsed_data.get_num_records()
            internal_val['original_format'] = parsed_data.get_original_format()
            internal_val['not_assigned_pct'] = parsed_data.get_not_assigned_pct()
            internal_val['y_value_counts'] = parsed_data.get_y_value_counts()

        return internal_val

    def validate(self, data):
        if self.queryset.exists({'user_id': data['user_id'],
                                 'name': data['name']}):
            raise serializers.ValidationError(
                f'You already have a dataset called {data["name"]}'
            )
        
        data['problem_type'] = validate_problem_type(data['problem_type'])

        return data
    
    def create(self):
        return Dataset.create(**self.validated_data)

    def save(self, dataset):
        if not isinstance(dataset, Dataset):
            raise TypeError('dataset must be of type Dataset')
        return self.queryset.save(dataset)
