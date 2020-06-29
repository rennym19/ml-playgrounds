from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock

from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.urls import reverse

from rest_framework import status

from bson import ObjectId

from mlplaygrounds.datasets.db.collections import MLModel
from mlplaygrounds.datasets.views.models import Models, ModelDetail
from .testcases import ModelViewTestCase


class TestModels(ModelViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:models')

    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.data')
    def test_get_user_models(self, mock_data):
        expected_models = self.dummy_data[0:2]
        for model in expected_models:
            model['uid'] = str(model.pop('_id'))
            model['dataset_id'] = str(model['dataset_id'])
            model['features'] = None
            model['coefficients'] = None
            model['error'] = None

        mock_data.return_value = expected_models

        response = self.client.get(self.url)

        self.assertListEqual(response.data, expected_models)

    def test_get_dataset_models(self):
        expected = self.dummy_data[1].copy()
        expected['uid'] = str(expected.pop('_id'))
        expected['dataset_id'] = str(expected['dataset_id'])
        expected['features'] = None
        expected['coefficients'] = None
        expected['error'] = None

        response = self.client.get(self.url, {
            'dataset_id': expected['dataset_id']
        })

        self.assertListEqual(response.data, [expected])

    def test_get_non_existant_dataset_models(self):
        response = self.client.get(self.url, {'dataset_id': ObjectId()})
        self.assertEqual(response.data, [])

    def test_get_models_by_invalid_id(self):
        response = self.client.get(self.url, {'dataset_id': '1234'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('mlplaygrounds.datasets.views.models.Models.get_trained_model')
    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.create')
    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.is_valid')
    def test_post_valid_model(self, mock_is_valid, mock_create, mock_trainer):
        expected = {
            'name': 'model',
            'algorithm': 'ml algorithm',
            'user_id': 'test_user',
            'dataset_id': 'test_dataset',
            'features': None,
            'coefficients': None,
            'error': None
        }
        mock_is_valid.return_value = True
        mock_create.return_value = MLModel.create(**expected)
        mock_trainer.return_value = Mock()

        response = self.client.post(self.url, expected, format='json')
        
        del response.data['uid']
        self.assertDictEqual(response.data, expected)

    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.errors',
           new_callable=PropertyMock(return_value=['Invalid Data']))
    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.is_valid')
    def test_post_invalid_model(self, mock_is_valid, mock_errors):
        mock_is_valid.return_value = False

        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    @patch('mlplaygrounds.datasets.views.models.Dataset.objects.get')
    def test_get_dataset(self, mock_get, mock_object_id):
        mock_get.return_value = Mock(uid='id')

        models_view = Models()
        res = models_view.get_dataset('id', 'user_id')

        self.assertEqual(res.uid, 'id')
    
    def test_get_dataset_no_id(self):
        with self.assertRaises(SuspiciousOperation):
            models_view = Models()
            models_view.get_dataset(None, 'user_id')
        
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    @patch('mlplaygrounds.datasets.views.models.Dataset.objects.get')
    def test_dataset_not_found(self, mock_get, mock_object_id):
        mock_get.return_value = None

        with self.assertRaises(Http404):
            models_view = Models()
            models_view.get_dataset('id', 'user_id')


class TestModelDetail(ModelViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:model-detail', args=['id'])

    def test_get_document(self):
        model_id = self.dummy_data[0]['_id']
        user_id = self.dummy_data[0]['user_id']

        model_detail_view = ModelDetail()
        document = model_detail_view.get_document(model_id, user_id)

        self.assertEqual(document, self.dummy_data[0])

    def test_get_non_existant_document(self):
        model_detail_view = ModelDetail()

        with self.assertRaises(Http404):
            model_detail_view.get_document('1234', 'fakeuser')

    @patch('mlplaygrounds.datasets.views.models.ModelDetail.get_document')
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    def test_get_object(self, mock_id, mock_document):
        mock_document.return_value = self.dummy_data[2]

        model_detail_view = ModelDetail()
        model = model_detail_view.get_object('model_id', 'user_id')

        self.assertEqual(str(model.uid), str(self.dummy_data[2]['_id']))
    
    def test_get_object_invalid_id(self):
        model_detail_view = ModelDetail()

        with self.assertRaises(SuspiciousOperation):
            model_detail_view.get_object('model_id', 'user_id')

    @patch('mlplaygrounds.datasets.views.models.ModelDetail.get_document')
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    def test_get_model(self, mock_id, mock_document):
        mock_document.return_value = self.dummy_data[0]

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('mlplaygrounds.datasets.views.models.MLModelSerializer.update')
    @patch('mlplaygrounds.datasets.views.models.ModelDetail.get_document')
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    def test_patch_model(self, mock_id, mock_document, mock_update):
        mock_document.return_value = self.dummy_data[0]
        mock_update.return_value = MLModel.create(**self.dummy_data[0])

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('mlplaygrounds.datasets.views.models.ModelDetail.get_document')
    @patch('mlplaygrounds.datasets.views.models.ObjectId')
    def test_delete_model(self, mock_id, mock_document):
        mock_document.return_value = self.dummy_data[2]

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
