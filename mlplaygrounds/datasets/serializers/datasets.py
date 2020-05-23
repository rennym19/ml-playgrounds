from rest_framework import serializers

from django.contrib.auth import get_user_model

from ..db.collections import Dataset


class DatasetSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=True
    )
    name = serializers.CharField(required=True)
    data = serializers.DictField(allow_empty=True, required=False)
    
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
