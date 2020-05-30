from unittest.mock import patch, MagicMock, PropertyMock

from django.urls import reverse

from rest_framework import status

from .testcases import DatasetViewTestCase


class TestParseDataset(DatasetViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:parse-dataset')

    @patch(
        'mlplaygrounds.datasets.views.datasets.DatasetSerializer',
        return_value=MagicMock
    )
    def test_parse_valid_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=True)
        serializer.create = MagicMock(return_value=MagicMock())
        serializer.save = MagicMock(return_value=MagicMock())
        serializer.data = PropertyMock(return_value={})

        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch(
        'mlplaygrounds.datasets.views.datasets.DatasetSerializer',
        return_value=MagicMock
    )
    def test_parse_invalid_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=False)
        serializer.errors = PropertyMock(return_value=['Invalid Data'])

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
