from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from django_mock_queries.query import MockModel

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.serializers import ValidationError

from mlplaygrounds.users.models import User


class TestLoginView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:login')
        self.valid_user = MockModel(username='test', password='password',
                                    email='test@mail.com', first_name='Test',
                                    last_name='Fake', registration_date=None)
        self.valid_token = 'token'
        self.setUpPatchers()

    def setUpPatchers(self):
        self.login_is_valid_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.is_valid',
            return_value=True
        )

        self.login_save_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.save',
            return_value=(self.valid_user, self.valid_token)
        )
        
        self.login_invalid_user_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.validate_username',
            side_effect=ValidationError('Invalid username')
        )

        self.login_invalid_password_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.validate',
            side_effect=ValidationError('Invalid password')
        )

    def test_login(self):
        data = {'username': 'test', 'password': 'password'}

        self.login_is_valid_patcher.start()
        self.login_save_patcher.start()
        
        response = self.client.post(self.url, data, format='json')

        self.login_is_valid_patcher.stop()
        self.login_save_patcher.stop()

        self.assertEqual(response.data['user']['username'], data['username'])
    
    def test_login_invalid_user(self):
        data = {'username': 'doesntexist', 'password': 'uselesspassword'}
        
        self.login_invalid_user_patcher.start()
        
        response = self.client.post(self.url, data, format='json')

        self.login_invalid_user_patcher.stop()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        data = {'username': 'test', 'password': 'wrong'}

        self.login_invalid_user_patcher.side_effect = None
        self.login_invalid_user_patcher.return_value = True
        self.login_invalid_user_patcher.start()
        self.login_invalid_password_patcher.start()

        response = self.client.post(self.url, data, format='json')

        self.login_invalid_user_patcher.stop()
        self.login_invalid_password_patcher.stop()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_already_logged_in(self):
        self.client.force_authenticate(user=MagicMock(username='test'))
        
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
