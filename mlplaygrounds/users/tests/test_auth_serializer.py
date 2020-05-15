from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from rest_framework.serializers import ValidationError

from django_mock_queries.query import MockSet, MockModel

from mlplaygrounds.users.serializers.auth import LoginSerializer

from mlplaygrounds.users.models import User


class TestLoginSerializer(TestCase):
    def test_login(self):
        data = {'username': 'test', 'password': 'password'}
        expected_user = User(**data)
        users = MockSet(
            expected_user
        )
        
        LoginSerializer._get_queryset = MagicMock(return_value=users)
        LoginSerializer.authenticate_user = MagicMock(return_value=expected_user) 

        serializer = LoginSerializer(data=data,
                                     context={'request': MagicMock()})

        with patch.object(User, 'check_password', return_value=True) as mocked_method:
            if serializer.is_valid():
                user = serializer.save()
                self.assertEqual(user.username, expected_user.username)

    def test_login_invalid_user(self):
        data = {'username': 'doesntexist', 'password': 'uselesspassword'}
        users = MockSet(
            MockModel(username='john', password='johnspassword'),
            MockModel(username='sarah', password='notjohnspassword')
        )

        LoginSerializer._get_queryset = MagicMock(return_value=users)
        
        serializer = LoginSerializer(data=data,
                                     context={'request': MagicMock()})

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_invalid_password(self):
        data = {'username': 'hacker', 'password': 'invalidpassword'}
        users = MockSet(
            User(**data)
        )

        LoginSerializer._get_queryset = MagicMock(return_value=users)

        serializer = LoginSerializer(data=data,
                                     context={'request': MagicMock()})
        
        with patch.object(User, 'check_password', return_value=False) as mocked_checker:
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)
