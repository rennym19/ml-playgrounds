from .connection import DATABASE_SETTINGS, db_client

from .type_casting import cast_document


class CollectionManager:
    def __init__(self, collection_name):
        self.COLLECTION_NAME = collection_name

        self._db_client = db_client
        self.db = self._db_client[DATABASE_SETTINGS['NAME']]
        self.collection = self.db[self.COLLECTION_NAME]

    def get(self, filter_by, cast_into_cls=None):
        document = self.collection.find_one(filter_by)
        return self._result(document, cast_into_cls=cast_into_cls)  

    def get_all(self, filter_by, limit=0, cast_into_cls=None):
        cursor = self.collection.find(filter_by, limit=limit)
        return self._result(list(cursor), True, cast_into_cls=cast_into_cls)

    def count(self, filter_by):
        return self.collection.count_documents(filter_by)

    def exists(self, filter_by):
        return True if self.count(filter_by) else False

    def insert(self, data={}):
        return self.collection.insert_one(data)

    def update(self, filter_by, update_fields, cast_into_cls=None):
        result = self.collection.update_one(filter_by, update_fields)
        return self._result(result.raw_result, cast_into_cls=cast_into_cls)

    def update_many(self, filter_by, update_fields, cast_into_cls=None):
        result = self.collection.update_many(filter_by, update_fields)
        return self._result(result.raw_result, many=True, cast_into_cls)
   
    def delete(self, filter_by):
        result = self.collection.delete_one(filter_by)
        return True if result.deleted_count else False

    def delete_many(self, filter_by):
        result = self.collection.delete_many(filter_by)
        return True if result.deleted_count else False

    def _result(self, doc, many=False, cast_into_cls=None):
        if cast_into_cls is not None:
            return cast_document(cast_into_cls, doc, many=many)
        return doc


class DatasetManager(CollectionManager):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def save(self, dataset):
        result = self.insert({'name': dataset.name,
                              'user_id': dataset.user_id,
                              'data': dataset.data})
        dataset.uid = result.inserted_id
        return dataset
