from unittest.mock import patch, MagicMock, PropertyMock

from django.urls import reverse

from rest_framework import status

from mlplaygrounds.datasets.parsers.parser import ParsedDataset
from mlplaygrounds.datasets.parsers.exceptions import InvalidFile
from .testcases import DatasetViewTestCase


class TestParseDataset(DatasetViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('datasets:parse-dataset')

        self.parser_patcher = patch(
            'mlplaygrounds.datasets.views.datasets.DatasetParser.parse',
            return_value=ParsedDataset({})
        )
        self.parser_patcher.start()

    @patch(
        'mlplaygrounds.datasets.views.datasets.DatasetSerializer',
        return_value=MagicMock
    )
    def test_serialize_valid_parsed_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=True)
        serializer.create = MagicMock(return_value=MagicMock())
        serializer.save = MagicMock(return_value=MagicMock())
        serializer.data = PropertyMock(return_value={})

        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('mlplaygrounds.datasets.views.datasets.DatasetSerializer')
    def test_serialize_invalid_parsed_data(self, mock_serializer):
        serializer = mock_serializer()
        serializer.is_valid = MagicMock(return_value=False)
        serializer.errors = ['Invalid']

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('mlplaygrounds.datasets.views.datasets.DatasetParser.parse')
    def test_parse_invalid_dataset(self, mock_parse):
        mock_parse.side_effect = InvalidFile('error')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
