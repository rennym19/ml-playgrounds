from unittest import TestCase

from ..db.collections import Dataset


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
            