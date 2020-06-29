from django.contrib.auth import get_user_model

from rest_framework import serializers

from bson import ObjectId
from bson.errors import InvalidId

from ..db.collections import MLModel, Dataset

User = get_user_model()


class MLModelSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    algorithm = serializers.CharField(required=True)
    dataset_id = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)
    features = serializers.ListField(required=False, default=None)
    coefficients = serializers.ListField(required=False, default=None)
    error = serializers.FloatField(required=False, default=None)

    REQUIRED_FIELDS = ['name', 'algorithm', 'dataset_id', 'user_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if isinstance(representation['uid'], ObjectId):
            representation['uid'] = str(representation['uid'])
        
        if isinstance(representation['dataset_id'], ObjectId):
            representation['dataset_id'] = str(representation['dataset_id'])

        return representation

    def to_internal_value(self, data):
        dataset_id = data.get('dataset_id', None)
        trained_model = data.get('trained_model', None)

        internal_val = {
            'user_id': data.get('user_id', None),
            'name': data.get('name', None),
            'algorithm': data.get('algorithm', None),
            'dataset_id': ObjectId(dataset_id) if dataset_id else None
        }

        if trained_model:
            internal_val['features'] = trained_model.features
            internal_val['coefficients'] = trained_model.coefficients()
            internal_val['error'] = trained_model.error()

        uid = data.get('uid', None)
        if not isinstance(uid, ObjectId) and uid is not None:
            internal_val['uid'] = ObjectId(data['uid'])

        return internal_val

    def validate(self, data):
        for field in self.REQUIRED_FIELDS:
            self.validate_field_set(data, field)

        data['dataset_id'] = self.validate_dataset_id(data['dataset_id'])
        data['user_id'] = self.validate_user_id(data['user_id'])

        return data

    def validate_field_set(self, data, val):
        if val not in data:
            raise serializers.ValidationError(f'{val} not in data')

    def validate_dataset_id(self, id):
        object_id = None
        try:
            object_id = ObjectId(id)
        except (TypeError, InvalidId):
            raise serializers.ValidationError('Invalid ID')

        if Dataset.objects.exists({'_id': object_id}):
            return object_id
        raise serializers.ValidationError(f'No Dataset exists with ID {id}')

    def validate_user_id(self, id):
        if User.objects.filter(username=id).exists():
            return id
        raise serializers.ValidationError(f'No user exists with ID {id}')

    def create(self):
        return MLModel.create(**self.validated_data)
    
    def update(self, instance, validated_data):
        if instance:
            for field, val in validated_data.items():
                self.update_field(instance, field, val)
            updated = MLModel.objects.update({'_id': instance.uid},
                                             validated_data)
            if updated:
                return instance
            raise ValueError('Instance could not be updated.'
                             'It probably does not exist')
        raise ValueError('Could not update: instance needed')

    def update_field(self, instance, field, val):
        setattr(instance, field, val)
        
    def save(self, model):
        if not isinstance(model, MLModel):
            raise TypeError('model must be of type MLModel')
        return MLModel.objects.save(model)


class MLModelLiteSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    algorithm = serializers.CharField(required=True)
