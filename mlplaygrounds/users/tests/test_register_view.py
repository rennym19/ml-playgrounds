from unittest import TestCase
from unittest.mock import patch, PropertyMock

from django_mock_queries.query import MockModel

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from mlplaygrounds.users.models import User


class TestRegistrationView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:register')
        
        self.valid_data = {'username': 'john', 'email': 'john@mail.com',
                           'last_name': 'Appleseed', 'first_name': 'John',
                           'registration_date': None}
        self.valid_token = 'token'

        self.setUpPatchers()

    def setUpPatchers(self):
        self.register_is_valid_patcher = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.is_valid',
            return_value=True
        )

        self.register_validated_data_patcher = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.validated_data',
            new_callable=PropertyMock(return_value=self.valid_data)
        )

        self.register_create_patcher = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.create',
            return_value=MockModel(username=self.valid_data['username'])
        )

        self.register_login_patch = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.login',
            return_value=self.valid_token
        )

        self.user_serializer_data_patcher = patch(
            'mlplaygrounds.users.views.auth.UserSerializer.data',
            new_callable=PropertyMock(return_value=self.valid_data)
        )

        self.register_invalid_data_patcher = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.is_valid',
            return_value=False
        )

        self.register_errors_patcher = patch(
            'mlplaygrounds.users.views.auth.RegisterSerializer.errors',
            new_callable=PropertyMock(return_value={'errors': 'Invalid'})
        )

    def test_register(self):
        self.register_is_valid_patcher.start()
        self.register_validated_data_patcher.start()
        self.register_create_patcher.start()
        self.register_login_patch.start()
        self.user_serializer_data_patcher.start()

        response = self.client.post(self.url, {}, format='json')
    
        self.register_is_valid_patcher.stop()
        self.register_validated_data_patcher.stop()
        self.register_create_patcher.stop()
        self.register_login_patch.stop()
        self.user_serializer_data_patcher.stop()

        self.assertDictEqual(
            response.data, {'user': self.valid_data, 'token': self.valid_token})
    
    def test_register_with_invalid_data(self):
        self.register_invalid_data_patcher.start()
        self.register_errors_patcher.start()

        response = self.client.post(self.url, {}, format='json')
        
        self.register_invalid_data_patcher.stop()
        self.register_errors_patcher.stop()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_logged_in_user(self):
        self.client.force_authenticate(user=User(username='test'))
        
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
