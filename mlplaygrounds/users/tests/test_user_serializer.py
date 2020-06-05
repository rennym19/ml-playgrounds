from unittest import TestCase
from unittest.mock import patch

from django_mock_queries.query import MockModel

from django.utils.timezone import now

from rest_framework.serializers import ValidationError

from mlplaygrounds.users.serializers.users import UserSerializer


class TestUserSerializer(TestCase):
    def test_instance_serialization(self):
        registration_date = now()
        user = MockModel(username='test', email='test@mail.com',
                         first_name='Test', last_name='Fake',
                         registration_date=registration_date,
                         datasets=[MockModel(uid='1234',
                                             name='example_dataset')])
        expected_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'registration_date': user.registration_date.strftime(
                '%b %d, %Y, %H:%M %P'
            ),
            'datasets': [{
                'uid': user.datasets[0].uid,
                'name': user.datasets[0].name,
                'user_id': None
            }]
        }

        serialized_data = UserSerializer(user).data

        self.assertDictEqual(expected_data, serialized_data)

    def test_serialize_unvalid_data(self):
        data = {}

        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
