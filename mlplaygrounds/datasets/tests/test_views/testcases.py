from unittest import TestCase
from unittest.mock import PropertyMock, patch

from bson import ObjectId

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from mlplaygrounds.datasets.db.collections import Dataset, MLModel
from ..mocks.managers import MockDatasetManager, MockMLModelManager 

User = get_user_model()


class ViewTestCase(TestCase):
    def setUp(self):
        self.setUpClient()
    
    def setUpClient(self):
        self.user = User(username='john', email='john@appleseed.com',
                    first_name='John', last_name='Appleseed')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class DatasetViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.setUpMocks()

    def setUpMocks(self):
        self.dummy_data = [
            {
                '_id': ObjectId(),
                'name': 'First Dataset',
                'user_id': 'john',
                'data': {'foo': 'bar'},
                'problem_type': 'test'
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


class ModelViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.setUpMocks()
    
    def tearDown(self):
        self.stopManagerPatcher()

    def setUpMocks(self):
        self.dummy_data = [
            {
                '_id': ObjectId(),
                'name': 'Model',
                'user_id': 'john',
                'dataset_id': ObjectId(),
                'algorithm': 'SVM',
            },
            {
                '_id': ObjectId(),
                'name': 'Model Num. 2',
                'user_id': 'john',
                'dataset_id': ObjectId(),
                'algorithm': 'Decission Tree',
            },
            {
                '_id': ObjectId(),
                'name': 'Mike\'s Model',
                'user_id': 'mike',
                'dataset_id': ObjectId(),
                'algorithm': 'Linear Regression',
            }
        ]

        mocked_manager = MockMLModelManager()
        mocked_manager.collection.insert_many(self.dummy_data)
        self.startManagerPatcher(mocked_manager)
    
    def startManagerPatcher(self, mocked_manager):
        self.manager_patcher = patch(
            'mlplaygrounds.datasets.views.models.MLModel.objects',
            new_callable=PropertyMock(return_value=mocked_manager)
        )
        self.manager_patcher.start()
    
    def stopManagerPatcher(self):
        self.manager_patcher.stop()
