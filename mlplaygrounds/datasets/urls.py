from django.urls import path

from .views.datasets import Datasets, DatasetDetail, parse_dataset

app_name = 'datasets'
urlpatterns = [
    path('datasets/', Datasets.as_view(), name='datasets'),
    path('datasets/<uid>/', DatasetDetail.as_view(), name='dataset-detail'),
    path('parse_dataset/', parse_dataset, name='parse-dataset')
]
