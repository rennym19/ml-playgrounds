from django.conf import settings
from pymongo import MongoClient


DATABASE_SETTINGS = settings.DATABASES['default']
db_client = MongoClient(DATABASE_SETTINGS['HOST'], DATABASE_SETTINGS['PORT'])


def get_connection(db_name):
    return db_client[db_name]
