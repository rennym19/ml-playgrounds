from rest_framework import serializers

from mlplaygrounds.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'registration_date']
        extra_kwargs = {'password': {'write_only': True}}
