from unittest import TestCase
from unittest.mock import patch, PropertyMock

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from mlplaygrounds.users.models import User


class TestProfileEndpoint(TestCase):
    def test_get_profile(self):
        user = User(username='test', email='test@mail.com',
                    first_name='Test', last_name='Fake')
        expected_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'registration_date': None
        }

        with patch('mlplaygrounds.users.serializers.users.UserSerializer.data',
                new_callable=PropertyMock) as mocked_data:
            mocked_data.return_value = expected_data

            client = APIClient()
            client.force_authenticate(user=user)
            response = client.get(reverse('users:profile'))

            self.assertDictEqual(response.data, expected_data)

    def test_error_raised_when_user_not_logged_in(self):
        client = APIClient()
        response = client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
