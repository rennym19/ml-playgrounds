from unittest.mock import patch, PropertyMock, MagicMock

from django.urls import reverse

from rest_framework import status

from .testcases import DatasetViewTestCase


class TestDatasetsViews(DatasetViewTestCase):    
    @patch('mlplaygrounds.datasets.views.datasets.DatasetSerializer.data')
    def test_get(self, mock_data):
        expected_document = {
            'uid': str(self.dummy_data[0]['_id']),
            'name': self.dummy_data[0]['name'],
            'user_id': self.dummy_data[0]['user_id'],
            'problem_type': self.dummy_data[0]['problem_type']
        }
        mock_data.return_value = [expected_document]

        response = self.client.get(reverse('datasets:datasets'))

        self.assertDictEqual(response.data[0], expected_document)
    
    @patch(
        'mlplaygrounds.datasets.views.datasets.DatasetSerializer',
        return_value=MagicMock
    )
    def test_post_valid_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=True)
        serializer.save = MagicMock(return_value=MagicMock())
        serializer.create = MagicMock(return_value=MagicMock())
        serializer.data = PropertyMock(return_value={})

        response = self.client.post(reverse('datasets:datasets'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @patch(
        'mlplaygrounds.datasets.views.datasets.DatasetSerializer',
        return_value=MagicMock
    )
    def test_post_invalid_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=False)
        serializer.errors = PropertyMock(return_value=['Invalid data'])

        response = self.client.post(reverse('datasets:datasets'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
