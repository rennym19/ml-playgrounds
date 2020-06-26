from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from bson import ObjectId

from .mocks.managers import MockMLModelManager
from ..db.collections import Dataset, MLModel, Collection


class TestCollection(TestCase):
    def setUp(self):
        self.fields = {'foo': 'bar'}

    def test_create(self):
        obj = Collection.create_instance(MagicMock, **self.fields)
        self.assertEqual(obj.foo, self.fields['foo'])

    def test_create_invalid_class(self):
        with self.assertRaises(ValueError):
            obj = Collection.create_instance('notclass', **self.fields)


class TestDatasetCollection(TestCase):
    def setUp(self):
        self.setUpMocks()
    
    def setUpMocks(self):
        self.mock_models = [
            {
                '_id': ObjectId(),
                'name': 'Model',
                'user_id': 'john',
                'dataset_id': ObjectId(),
                'algorithm': 'SVM',
            }
        ]

        mocked_manager = MockMLModelManager()
        mocked_manager.collection.insert_many(self.mock_models)
        self.startModelManagerPatcher(mocked_manager)
    
    def startModelManagerPatcher(self, mocked_manager):
        self.model_manager_patcher = patch(
            'mlplaygrounds.datasets.views.models.MLModel.objects',
            new_callable=PropertyMock(return_value=mocked_manager)
        )
        self.model_manager_patcher.start()
    
    def tearDown(self):
        self.model_manager_patcher.stop()

    def test_create(self):
        dataset = Dataset.create(name='johns dataset',
                                 user_id='john',
                                 data={'name': 'John'})
        self.assertEqual(dataset.name, 'johns dataset')
    
    def test_create_extra_fields(self):
        dataset = Dataset.create(age=40)
        self.assertEqual(dataset.age, 40)

    def test_get_models(self):
        dataset = Dataset.create(uid=self.mock_models[0]['dataset_id'],
                                 name='dataset',
                                 user_id=self.mock_models[0]['user_id'])

        self.assertEqual(dataset.models[0].uid, self.mock_models[0]['_id'])
    
    def test_get_models_unsaved_dataset(self):
        dataset = Dataset()
        self.assertListEqual(dataset.models, [])

    def test_access_non_existant_field(self):
        dataset = Dataset()
        with self.assertRaises(AttributeError):
            dataset.foo

    def test_to_string(self):
        dataset = Dataset.create(name='dataset', user_id='user')
        self.assertEqual(str(dataset), 'dataset by user')


class TestMLModelCollection(TestCase):
    def test_create(self):
        model = MLModel.create(dataset_id='test_id',
                               algorithm='alg',
                               model='model')
        self.assertEqual(model.algorithm, 'alg')

    def test_create_extra_fields(self):
        model = MLModel.create(complicated=False)
        self.assertEqual(model.complicated, False)

    def test_access_non_existant_field(self):
        model = MLModel()
        with self.assertRaises(AttributeError):
            model.field

    def test_to_string(self):
        model = MLModel.create(name='Model', algorithm='SVM')
        self.assertEqual(str(model), 'Model (SVM)')
