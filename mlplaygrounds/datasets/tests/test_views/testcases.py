from unittest import TestCase
from unittest.mock import PropertyMock

from bson import ObjectId

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from mlplaygrounds.datasets.db.collections import Dataset
from ..mocks.managers import MockDatasetManager

User = get_user_model()


class DatasetViewTestCase(TestCase):
    def setUp(self):
        self.setUpClient()
        self.setUpMocks()
    
    def setUpClient(self):
        self.user = User(username='john', email='john@appleseed.com',
                    first_name='John', last_name='Appleseed')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def setUpMocks(self):
        self.dummy_data = [
            {
                '_id': ObjectId(),
                'name': 'First Dataset',
                'user_id': 'john',
                'data': {'foo': 'bar'}
            },
            {
                '_id': ObjectId(),
                'name': 'Second Dataset',
                'user_id': 'mike',
                'data': {'numbers': [1, 2, 3]}
            }
        ]

        mocked_manager = MockDatasetManager()
        mocked_manager.collection.insert_many(self.dummy_data)

        self.mocked_dataset = Dataset
        self.mocked_dataset.objects = PropertyMock(return_value=mocked_manager)
