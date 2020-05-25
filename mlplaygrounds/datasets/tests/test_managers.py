from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock, Mock

import mongomock

from ..db.managers import CollectionManager, DatasetManager


class MockCollectionManager(CollectionManager):
    def __init__(self):
        self._db_client = mongomock.MongoClient()
        self.collection = self._db_client.db.collection
        
        self.dummy_data = [
            {'username': 'julia'},
            {'username': 'rita', 'age': 18},
            {'username': 'mike', 'age': 18},
            {'username': 'peter', 'age': 25},
            {'username': 'renny', 'admin': True, 'programmer': True}
        ]
        self.collection.insert_many(self.dummy_data)


class TestCollectionManager(TestCase):
    def setUp(self):
        self.manager = MockCollectionManager()

    def test_get(self):
        document = self.manager.get({'username': 'julia'}, {'_id': False})
        self.assertEqual(document, {'username': 'julia'})

    def test_get_all(self):
        documents = self.manager.get_all({})
        self.assertEqual(documents, self.manager.dummy_data)
    
    def test_count(self):
        self.assertEqual(self.manager.count({'programmer': True}), 1)
    
    def test_exists(self):
        self.assertEqual(self.manager.exists({'username': 'rita'}), True)

    def test_does_not_exist(self):
        self.assertEqual(self.manager.exists({'username': 'alexa'}), False)

    def test_insert(self):
        inserted_id = self.manager.insert({'username': 'john'})
        created_document = self.manager.get({'_id': inserted_id},
                                            projection={'_id': False})
        self.assertEqual(created_document, {'username': 'john'})

    def test_update_existing_field(self):
        updated_count = self.manager.update({'username': 'mike'},
                                            {'username': 'jeff'})
        self.assertEqual(updated_count, 1)
    
    def test_update_non_existing_field(self):
        updated_count = self.manager.update({'username': 'julia'},
                                            {'username': 'siri', 'human': False})

        self.assertEqual(updated_count, 1)

    def test_update_many(self):
        updated_count = self.manager.update_many({'age': 18}, {'age': 19})
        self.assertEqual(updated_count, 2)
    
    def test_delete(self):
        deleted_count = self.manager.delete({'username': 'peter'})
        self.assertEqual(deleted_count, 1)

    def test_delete_does_not_exist(self):
        deleted_count = self.manager.delete({'username': 'patrick'})
        self.assertEqual(deleted_count, 0)

    def test_delete_many(self):
        deleted_count = self.manager.delete_many({'age': 18})
        self.assertEqual(deleted_count, 2)

    def test_result_with_no_typecasting(self):
        res = self.manager._result({'username': 'jack'})
        self.assertEqual(res, {'username': 'jack'})
    
    @patch('mlplaygrounds.datasets.db.managers.cast_document',
           return_value=Mock(username='jack'))
    def test_result_with_typecasting(self, cast_mock):
        res = self.manager._result({'username': 'jack'},
                                   cast_into_cls=Mock)
        self.assertEqual(res.username, 'jack')


class MockDatasetManager(DatasetManager):
    def __init__(self):
        self._db_client = mongomock.MongoClient()
        self.collection = self._db_client.db.collection


class TestDatasetManager(TestCase):
    def setUp(self):
        self.manager = MockDatasetManager()

    def test_save(self):
        dataset = Mock()
        dataset.name = 'Dataset'
        dataset.user_id = 'john'
        dataset.data = {'a': 'b'}

        saved = self.manager.save(dataset)
        
        self.assertEqual([dataset.name, dataset.user_id, dataset.data],
                         [saved.name, saved.user_id, saved.data])
        self.assertIsNotNone(saved.uid)
