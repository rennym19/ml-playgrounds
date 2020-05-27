import mongomock

from mlplaygrounds.datasets.db.managers import (
    CollectionManager,
    DatasetManager
)


class MockCollectionManager(CollectionManager):
    def __init__(self):
        self._db_client = mongomock.MongoClient()
        self.collection = self._db_client.db.collection


class MockDatasetManager(DatasetManager):
    def __init__(self):
        self._db_client = mongomock.MongoClient()
        self.collection = self._db_client.db.collection
