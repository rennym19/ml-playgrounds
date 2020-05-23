from django.contrib.auth import get_user_model

from rest_framework import serializers

from bson.objectid import ObjectId

from ..db.collections import Dataset


class DatasetSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=True
    )
    name = serializers.CharField(required=True)
    data = serializers.DictField(allow_empty=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['uid'] = str(instance.uid)
        return representation
    
    def to_internal_value(self, data):
        internal_val = Dataset(**data)
        
        if not isinstance(data['uid'], ObjectId):
            internal_val.uid = ObjectId(data['uid'])
        
        return internal_val
    
    def validate_name(self, name):
        if len(name) > 255:
            raise serializers.ValidationError(
                'Name can\'t have more than 255 characters.'
            )
        return name
    
    def validate(self, data):
        if Dataset.objects.exists({'user_id': data['user_id'],
                                   'name': data['name']}):
            raise serializers.ValidationError(
                f'You already have a dataset called {data["name"]}'
            )
        return data
    
    def create(self):
        return Dataset.create(self.validated_data)

    def save(self, dataset):
        if not isinstance(dataset, Dataset):
            raise TypeError('dataset must be of type Dataset')
        return Dataset.objects.save(dataset)
