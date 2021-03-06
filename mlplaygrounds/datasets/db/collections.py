from inspect import isclass
from .managers import DatasetManager, MLModelManager


class Collection:
    @classmethod
    def create_instance(self, cls, **kwargs):
        if not isclass(cls):
            raise ValueError(f'Class needed in order to create instance.'
                              'Got {cls.__class__.__name__}')
        obj = cls()
        for field, val in kwargs.items():
            if field == '_id':
                setattr(obj, 'uid', val)
            else:
                setattr(obj, field, val)
        return obj


class Dataset(Collection):
    uid = None
    name = None
    data = None
    user_id = None

    class Meta:
        collection_name = 'datasets'

    objects = DatasetManager(Meta.collection_name)

    @classmethod
    def create(self, **kwargs):
        return Collection.create_instance(Dataset, **kwargs)

    @property
    def models(self):
        if self.uid and self.user_id:
            return MLModel.objects.get_all({'dataset_id': self.uid,
                                            'user_id': self.user_id},
                                           cast_into_cls=MLModel)
        return []

    def __str__(self):
        return f'{self.name} by {self.user_id}'


class MLModel(Collection):
    uid = None
    name = None
    user_id = None
    dataset_id = None
    algorithm = None

    class Meta:
        collection_name = 'models'

    objects = MLModelManager(Meta.collection_name)

    @classmethod
    def create(self, **kwargs):
        return Collection.create_instance(MLModel, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.algorithm})'
