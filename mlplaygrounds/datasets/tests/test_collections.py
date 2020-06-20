from unittest import TestCase
from unittest.mock import MagicMock

from ..db.collections import Dataset, MLModel, Collection


class TestCollection(TestCase):
    def setUp(self):
        self.collection_fields = {'foo': 'bar'}

    def test_create(self):
        obj = Collection.create_instance(MagicMock, **self.collection_fields)
        self.assertEqual(obj.foo, self.collection_fields['foo'])

    def test_create_invalid_class(self):
        with self.assertRaises(ValueError):
            obj = Collection.create_instance('notclass',
                                             **self.collection_fields)


class TestDatasetCollection(TestCase):
    def test_create(self):
        dataset = Dataset.create(name='johns dataset',
                                 user_id='john',
                                 data={'name': 'John'})
        self.assertEqual(dataset.name, 'johns dataset')
    
    def test_create_extra_fields(self):
        dataset = Dataset.create(age=40)
        self.assertEqual(dataset.age, 40)

    def test_access_non_existant_field(self):
        dataset = Dataset()
        with self.assertRaises(AttributeError):
            dataset.foo

    def test_to_string(self):
        dataset = Dataset.create(name='dataset',
                                 user_id='user')
        
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
