from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from rest_framework.serializers import ValidationError

from django_mock_queries.query import MockSet, MockModel

from ..serializers.auth import LoginSerializer, RegisterSerializer

from ..models import User


class TestLoginSerializer(TestCase):
    def setUp(self):
        self.valid_data = {'username': 'test', 'password': 'password'}
        self.valid_user = User(**self.valid_data)
        self.setUpPatchers()

    def setUpPatchers(self):
        self.authenticate_patcher = patch(
            'mlplaygrounds.users.serializers.auth.authenticate',
            return_value=self.valid_user
        )

        self.authenticate_failed_patcher = patch(
            'mlplaygrounds.users.serializers.auth.authenticate',
            return_value=None
        )

    def test_login(self):
        users = MockSet(self.valid_user)
        
        LoginSerializer._get_queryset = MagicMock(return_value=users)
        LoginSerializer.save = MagicMock(return_value=(self.valid_user, 'token')) 
        self.authenticate_patcher.start()

        serializer = LoginSerializer(data=self.valid_data)

        if serializer.is_valid():
            user, token = serializer.save()
            self.assertEqual(user.username, self.valid_user.username)
            self.assertEqual(token, 'token')

        self.authenticate_patcher.stop()

    def test_login_invalid_user(self):
        data = {'username': 'doesntexist', 'password': 'uselesspassword'}
        users = MockSet(
            MockModel(username='john', password='johnspassword'),
            MockModel(username='sarah', password='notjohnspassword')
        )

        LoginSerializer._get_queryset = MagicMock(return_value=users)
        
        serializer = LoginSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_invalid_password(self):
        data = {'username': 'hacker', 'password': 'invalidpassword'}
        users = MockSet(
            User(**data)
        )

        LoginSerializer._get_queryset = MagicMock(return_value=users)
        self.authenticate_failed_patcher.start()

        serializer = LoginSerializer(data=data)
        
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        self.authenticate_failed_patcher.stop()


class TestRegisterSerializer(TestCase):
    def setUp(self):
        self.users = MockSet(
            MockModel(username='nottest', email='nottest@mail.com'),
            MockModel(username='test', email='test@mail.com')
        )
        self.users.create_user = MagicMock(
            return_value=MockModel(username='john'))

        RegisterSerializer._get_queryset = MagicMock(return_value=self.users)
    
    def test_create(self):
        data = {'username': 'john', 'password': 'Appleseed.123',
                'email': 'john@mail.com', 'first_name': 'John',
                'last_name': 'Appleseed'}

        serializer = RegisterSerializer(data=data,
                                        context={'request': MagicMock()})
        
        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        created_user = serializer.create(serializer.validated_data)
        self.assertEqual(created_user.username, data['username'])

    def test_invalid_user(self):
        data = {'username': 'test', 'password': 'ValidPassword.123',
                'email': 'anothertest@mail.com', 'first_name': 'Tester',
                'last_name': 'Tested'}
        
        serializer = RegisterSerializer(data=data,
                                        context={'request': MagicMock()})

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_password(self):
        data = {'username': 'validuser', 'password': 't123',
                'email': 'anothertest@mail.com', 'first_name': 'Tester',
                'last_name': 'Tested'}

        serializer = RegisterSerializer(data=data,
                                        context={'request': MagicMock()})

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
