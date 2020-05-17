from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from django_mock_queries.query import MockSet, MockModel

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.serializers import ValidationError

from mlplaygrounds.users.views.auth import Logout
from mlplaygrounds.users.models import User


class TestLoginView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:login')
        self.setUpPatchers()

    def setUpPatchers(self):
        self.login_is_valid_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.is_valid',
            return_value=True
        )

        self.login_save_patcher = patch(
            'mlplaygrounds.users.views.auth.LoginSerializer.save',
            return_value=MagicMock(username='test')
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

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
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


class TestLogoutView(TestCase):
    def setUp(self):
        self.url = reverse('users:logout')
        self.client = APIClient()

    def test_logout(self):
        user = User(username='test', password='p')
        
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_logout_unauthenticated_user(self):
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRegistrationView(TestCase):
    def test_register(self):
        pass
    
    def test_register_user_with_incomplete_data(self):
        pass

    def test_register_user_with_invalid_credentials(self):
        pass
