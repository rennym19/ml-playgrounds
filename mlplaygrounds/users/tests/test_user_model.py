from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from bson import ObjectId

from django_mock_queries.query import MockSet

from mlplaygrounds.datasets.tests.mocks.managers import MockDatasetManager
from ..models import User, CustomUserManager


class TestUserModel(TestCase):
    def setUp(self):
        mock_manager = MockDatasetManager()
        mock_manager.collection.insert_many([
            {'_id': 1, 'user_id': 'john', 'name': 'jdata', 'data': {}},
            {'_id': 2, 'user_id': 'test', 'name': 'test', 'data': {}}
        ])

        self.manager_patcher = patch(
            'mlplaygrounds.users.models.Dataset.objects',
            new_callable=PropertyMock(return_value=mock_manager)
        )

        self.manager_patcher.start()

    def test_datasets(self):
        expected_dataset = {'uid': 2, 'name': 'test'}

        user = User()
        user.username = 'test'

        user_datasets = [
            {'uid': dataset.uid, 'name': dataset.name}
            for dataset in user.datasets
        ]

        self.assertEqual(user_datasets, [expected_dataset])

    def tearDown(self):
        self.manager_patcher.stop()


class TestUserManager(TestCase):
    def setUp(self):
        self.save_patcher = patch(
            'mlplaygrounds.users.models.User.save',
            return_value=MagicMock()
        )
        self.save_patcher.start()
       
    def tearDown(self):
        self.save_patcher.stop()

    @patch('mlplaygrounds.users.models.CustomUserManager._credentials_already_in_use')
    def test_create_user(self, mock_credentials_in_use):
        mock_credentials_in_use.return_value = False

        manager = CustomUserManager()
        user = manager.create_user('usr', 'pass', 'email', 'name', 'sname')

        self.assertEqual(user.username, 'usr')

    @patch('mlplaygrounds.users.models.CustomUserManager._credentials_already_in_use')
    def test_create_invalid_user(self, mock_credentials_in_use):
        mock_credentials_in_use.return_value = True

        manager = CustomUserManager() 
        
        with self.assertRaises(ValueError):
            manager.create_user('usr', 'pass', 'email', 'name', 'sname')

    @patch('mlplaygrounds.users.models.CustomUserManager._credentials_already_in_use')
    def test_create_superuser(self, mock_credentials_in_use):
        mock_credentials_in_use.return_value = False

        manager = CustomUserManager()
        user = manager.create_superuser('susr', 'pass', 'semail', 'name', 'sname')

        self.assertEqual(user.is_superuser, True)
    
    @patch('mlplaygrounds.users.models.CustomUserManager._credentials_already_in_use')
    def test_create_invalid_superuser(self, mock_credentials_in_use):
        mock_credentials_in_use.return_value = True

        manager = CustomUserManager() 
        
        with self.assertRaises(ValueError):
            manager.create_superuser('susr', 'pass', 'semail', 'name', 'sname')

    @patch('mlplaygrounds.users.models.User.objects')
    def test_check_credentials_in_use(self, mock_objects):
        mock_objects.filter.return_value = mock_objects
        mock_objects.exists.return_value = True

        manager = CustomUserManager()
        in_use = manager._credentials_already_in_use('mary', 'mail@mail.com')

        self.assertEqual(in_use, True)

    @patch('mlplaygrounds.users.models.User.objects')
    def test_check_credentials_not_in_use(self, mock_objects):
        mock_objects.filter.return_value = mock_objects
        mock_objects.exists.return_value = False

        manager = CustomUserManager() 
        in_use = manager._credentials_already_in_use('patrick', 'p@mail.com')

        self.assertEqual(in_use, False)
