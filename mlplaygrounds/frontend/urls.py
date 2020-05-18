from django.urls import path

from mlplaygrounds.frontend.views.index import index

urlpatterns = [
    path('', index),
]