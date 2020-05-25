from django.db import models

from .managers import DatasetManager


class Dataset:
    uid = None
    name = None
    data = None
    user_id = None

    class Meta:
        collection_name = 'datasets'

    objects = DatasetManager(Meta.collection_name)

    @staticmethod
    def create(**kwargs):
        dataset = Dataset()
        for field, val in kwargs.items():
            setattr(dataset, field, val)
        return dataset

    def __str__(self):
        return f'{self.name} by {self.user_id}'
