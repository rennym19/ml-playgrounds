from django.urls import path

from .views.datasets import Datasets

app_name = 'datasets'
urlpatterns = [
    path('datasets/', Datasets.as_view(), name='datasets')
]
