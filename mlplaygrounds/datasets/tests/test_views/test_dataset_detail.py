from unittest.mock import patch, PropertyMock, MagicMock

from django_mock_queries.query import MockModel

from django.urls import reverse
from django.http import Http404

from rest_framework import status
from rest_framework.serializers import ValidationError

from mlplaygrounds.datasets.views.datasets import DatasetDetail
from mlplaygrounds.datasets.db.collections import Dataset
from .testcases import DatasetViewTestCase


class TestDatasetDetailViews(DatasetViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:dataset-detail', args=['id'])

    @patch('mlplaygrounds.datasets.views.datasets.DatasetDetail.get_object',
           return_value=MagicMock())
    @patch('mlplaygrounds.datasets.views.datasets.DatasetSerializer.data',
           new_callable=PropertyMock)
    def test_get(self, mock_get_object, mock_serializer_data):
        mock_get_object.return_value = {}
        mock_serializer_data.return_value = {}

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('mlplaygrounds.datasets.views.datasets.DatasetDetail.get_object',
           return_value=MagicMock())
    def test_update_valid_data(self, mock_get_object):
        mock_get_object.return_value = Dataset()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('mlplaygrounds.datasets.views.datasets.DatasetDetail.get_object',
           return_value=MagicMock())
    @patch('mlplaygrounds.datasets.views.datasets.DatasetSerializer.is_valid',
           return_value=False)
    @patch('mlplaygrounds.datasets.views.datasets.DatasetSerializer.errors',
           new_callable=PropertyMock(return_value=['Invalid']))
    def test_update_invalid_data(self, mock_get_obj, mock_is_valid, mock_err):
        response = self.client.put(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        'mlplaygrounds.datasets.views.datasets.Dataset.objects.delete',
        return_value=MagicMock()
    )
    def test_delete(self, mock_delete):
        mock_delete.return_value = 1
        
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch(
        'mlplaygrounds.datasets.views.datasets.Dataset.objects.delete',
        return_value=MagicMock()
    )
    def test_delete_non_existant_dataset(self, mock_delete):
        mock_delete.return_value = 0

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch(
        'mlplaygrounds.datasets.views.datasets.Dataset.objects.get',
        return_value=MagicMock()
    )
    def test_get_document(self, mock_get):
        mock_get.return_value = {'name': 'test'}

        view = DatasetDetail()
        document = view.get_document('id', 'user_id')

        self.assertEqual(document, {'name': 'test'})

    @patch(
        'mlplaygrounds.datasets.views.datasets.Dataset.objects.get',
        return_value=MagicMock()
    )
    def test_get_non_existant_document(self, mock_get):
        mock_get.side_effect = Http404

        view = DatasetDetail()
        
        with self.assertRaises(Http404):
            view.get_document('id', 'user_id')

    @patch('mlplaygrounds.datasets.views.datasets.DatasetDetail.get_document')
    def test_get_object(self, mock_get_document):
        document = {'name': 'test', 'user_id': 'user', 'data': {'foo': 'bar'}}
        mock_get_document.return_value = document

        view = DatasetDetail()
        dataset = view.get_object(str(self.dummy_data[0]['_id']),
                                  self.dummy_data[0]['user_id'])

        object_data = {
            'name': dataset.name,
            'user_id': dataset.user_id,
            'data': dataset.data
        }
        self.assertDictEqual(document, object_data)
