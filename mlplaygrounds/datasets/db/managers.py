from .connection import DATABASE_SETTINGS, db_client

from .type_casting import cast_document


class CollectionManager:
    def __init__(self, collection_name, collection_cls=None):
        self.COLLECTION_NAME = collection_name
        self.collection_cls = collection_name

        self._db_client = db_client
        self.db = self._db_client[DATABASE_SETTINGS['NAME']]
        self.collection = self.db[self.COLLECTION_NAME]

    def get(self, filter_by, cast_into_cls=False):
        document = self.collection.find_one(filter_by)
        return self._result(document, cast_into_cls=cast_into_cls)  

    def get_all(self, filter_by, limit=0, cast_into_cls=False):
        cursor = self.collection.find(filter_by, limit=limit)
        return self._result(list(cursor), True, cast_into_cls=cast_into_cls)

    def count(self, filter_by):
        return self.collection.count_documents(filter_by)

    def exists(self, filter_by):
        return True if self.count(filter_by) else False

    def insert(self, data={}):
        return self.collection.insert_one(data)

    def update(self, filter_by, update_fields, cast_into_cls=False):
        result = self.collection.update_one(filter_by, update_fields)
        return (
            result.modified_count,
            self._result(result.raw_result, cast_into_cls=cast_into_cls)
        )
    
    def delete(self, filter_by):
        result = self.collection.delete_many(filter_by)
        return result.deleted_count

    def _result(self, doc, many=False, cast_into_cls=False):
        if self.collection_cls is not None and cast_into_cls:
            return cast_document(self.collection_cls, doc, many=many)
        return doc


class DatasetManager(CollectionManager):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def save(self, dataset):
        uid = self.insert({'name': dataset.name,
                           'user_id': dataset.user_id,
                           'data': dataset.data})
        dataset.uid = uid
        return dataset
