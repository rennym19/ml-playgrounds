from .connection import DATABASE_SETTINGS, db_client

from .type_casting import cast_document


class CollectionManager:
    def __init__(self, database_name, collection_name):
        self.COLLECTION_NAME = collection_name

        self._db_client = db_client
        self.db = self._db_client[database_name]
        self.collection = self.db[self.COLLECTION_NAME]

    def get(self, filter_by, projection=None, cast_into_cls=None):
        if projection is None:
            document = self.collection.find_one(filter_by)
        else:
            document = self.collection.find_one(filter_by,
                                                projection=projection)
        
        return self._result(document, cast_into_cls=cast_into_cls)  

    def get_all(self, filter_by, projection=None, limit=0, cast_into_cls=None):
        cursor = self.collection.find(filter_by, projection, limit=limit)
        return self._result(list(cursor), True, cast_into_cls=cast_into_cls)

    def count(self, filter_by):
        return self.collection.count_documents(filter_by)

    def exists(self, filter_by):
        return True if self.count(filter_by) else False

    def insert(self, data={}):
        return self.collection.insert_one(data).inserted_id

    def update(self, filter_by, update_fields, cast_into_cls=None):
        result = self.collection.update_one(filter_by,
                                            {'$inc': update_fields})
        return result.modified_count

    def update_many(self, filter_by, update_fields, cast_into_cls=None):
        result = self.collection.update_many(filter_by,
                                             {'$inc': update_fields})
        return result.modified_count
   
    def delete(self, filter_by):
        result = self.collection.delete_one(filter_by)
        return result.deleted_count

    def delete_many(self, filter_by):
        result = self.collection.delete_many(filter_by)
        return result.deleted_count

    def _result(self, doc, many=False, cast_into_cls=None):
        if cast_into_cls is not None:
            return cast_document(cast_into_cls, doc, many=many)
        return doc


class DatasetManager(CollectionManager):
    def __init__(self, collection_name):
        super().__init__(DATABASE_SETTINGS['NAME'], collection_name)
    
    def save(self, dataset):
        dataset.uid = self.insert(dataset.__dict__)
        return dataset
