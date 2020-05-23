from django.db import models
from django.contrib.auth import get_user_model

from .managers import CollectionManager


class Dataset:
    uid = None
    name = None
    data = None
    user_id = None

    class Meta:
        collection_name = 'datasets'

    objects = CollectionManager(Meta.collection_name)

    def __str__(self):
        return f'{self.name} by {self.user_id}'
