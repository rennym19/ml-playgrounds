from django.db import models
from django.contrib.auth import get_user_model

from .managers import DatasetManager


class Dataset:
    uid = None
    name = None
    data = None
    user_id = None

    class Meta:
        collection_name = 'datasets'

    objects = DatasetManager(Meta.collection_name)

    def create(self, **kwargs):
        dataset = Dataset()
        for k, v in kwargs.items():
            setattr(dataset, k, v)
        return dataset

    def __str__(self):
        return f'{self.name} by {self.user_id}'
