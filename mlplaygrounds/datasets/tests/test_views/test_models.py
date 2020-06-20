from unittest import TestCase
from unittest.mock import patch

from django.urls import reverse

from rest_framework import status

from bson import ObjectId

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

        mock_data.return_value = expected_models

        response = self.client.get(self.url)

        self.assertListEqual(response.data, expected_models)

    def test_get_dataset_models(self):
        expected = self.dummy_data[1].copy()
        expected['uid'] = str(expected.pop('_id'))
        expected['dataset_id'] = str(expected['dataset_id'])

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

    def test_post_valid_model(self):
        pass

    def test_post_invalid_model(self):
        pass


class TestModelDetail(ModelViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:model-detail', args=['id'])

    def test_get_model(self):
        pass

    def test_get_invalid_model(self):
        pass
