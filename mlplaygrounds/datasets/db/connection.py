from django.conf import settings
from pymongo import MongoClient


class ConnectionManager:
    def __init__(self):
        self.DATABASE_SETTINGS = settings.DATABASES['default']
        self._client = MongoClient(self.DATABASE_SETTINGS['HOST'],
                                   self.DATABASE_SETTINGS['PORT'])
        self._db = self._client[self.DATABASE_SETTINGS['NAME']]
    
    def get_connection(self):
        return self._db


class MongoAccessObject:
    def __init__(self):
        self.COLLECTION_NAME = 'databank'

        self._connection_manager = ConnectionManager()
        self.db = self._connection_manager.get_connection()
        self.collection = self.db[self.COLLECTION_NAME]
    
    def get(self, user_id, dataset_id):
        document = self.collection.find_one({'user_id': user_id,
                                             'dataset_id': dataset_id})
        return document

    def get_all(self, filter_by):
        return self.collection.find(filter_by)

    def count(self, filter_by):
        return self.collection.count_documents(filter_by)

    def insert(self, user_id, dataset_id, data={}):
        self.collection.insert_one({'user_id': user_id,
                                    'dataset_id': dataset_id,
                                    'data': data})

    def update(self, filter_by, update_fields):
        result = self.collection.update_one(filter_by, update_fields)
        return (result.modified_count, result.raw_result)
    
    def delete(self, filter_by):
        result = self.collection.delete_many(filter_by)
        return result.deleted_count
