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
