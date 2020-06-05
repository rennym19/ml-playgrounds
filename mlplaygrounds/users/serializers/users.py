from rest_framework import serializers

from mlplaygrounds.datasets.serializers.datasets import DatasetSerializer
from mlplaygrounds.users.models import User


class UserSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True, read_only=True, exclude_data=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'registration_date', 'datasets']
        extra_kwargs = {'password': {'write_only': True},
                        'datasets': {'read_only': True}}
