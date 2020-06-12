from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from django_mock_queries.query import MockModel, MockSet

from bson import ObjectId

from django.contrib.auth import get_user_model

from rest_framework import serializers

from ..db.collections import Dataset
from ..parsers.parser import ParsedDataset
from ..serializers.datasets import DatasetSerializer
from .mocks.managers import MockDatasetManager


class TestDatasetSerializer(TestCase):
    def setUp(self):
        self.valid_instance = MockModel(name='Dataset',
                                        user_id='testuser',
                                        data={'id': 1, 'foo': 'bar', 'bool': True},
                                        index_col='id',
                                        label='foo',
                                        label_data='bar',
                                        num_records=1,
                                        features=['foo', 'bar'],
                                        original_format='csv',
                                        not_assigned_pct=0)
        
        self.expected_valid_instance_data = {
            'uid': None,
            'name': self.valid_instance.name,
            'user_id': self.valid_instance.user_id,
            'data': self.valid_instance.data,
            'index_col': self.valid_instance.index_col,
            'label': self.valid_instance.label,
            'label_data': self.valid_instance.label_data,
            'num_records': self.valid_instance.num_records,
            'features': self.valid_instance.features,
            'original_format': self.valid_instance.original_format,
            'not_assigned_pct': self.valid_instance.not_assigned_pct
        }

    def test_instance_serialization(self):
        serializer = DatasetSerializer(self.valid_instance)

        self.assertDictEqual(serializer.data,
                             self.expected_valid_instance_data)

    def test_instance_serialization_with_id(self):
        self.valid_instance.uid = ObjectId()
        self.expected_valid_instance_data['uid'] = str(self.valid_instance.uid)
        
        serializer = DatasetSerializer(self.valid_instance)
        
        self.assertDictEqual(serializer.data,
                             self.expected_valid_instance_data)

    def test_many_instances_serialization(self):
        instances = [ 
            MockModel(uid=ObjectId(), name='A', user_id='u', data={'a': 'b'}),
            MockModel(uid=ObjectId(), name='B', user_id='u', data={'a': 'b'})
        ]
        expected_data = [
            {'uid': str(instance.uid),
             'name': instance.name,
             'user_id': instance.user_id}
            for instance in instances
        ]

        serializer = DatasetSerializer(instances, many=True, exclude_data=True)

        self.assertCountEqual(serializer.data, expected_data)

    def test_serialize_valid_data(self):
        data = {
            'name': 'Dataset',
            'user_id': 'testuser',
            'data': {'foo': 'bar', 'inner': {'nested': True}}
        }

        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(
            return_value=MockDatasetManager())
        mocked_serializer._get_queryset.exists = MagicMock(return_value=False)
        
        serializer = mocked_serializer(data=data)

        self.assertEqual(serializer.is_valid(), True)
    
    def test_create_instance_from_parsed_dataset(self):
        mock_data = MagicMock(ParsedDataset)
        mock_data.get_data.return_value = [{'foo': 'bar'}]
        mock_data.get_index_col.return_value = 'test_id'
        mock_data.get_features.return_value = ['test_col1', 'test_col2']
        mock_data.get_label.return_value = 'test_label_col'
        mock_data.get_label_data.return_value = 'test_label'
        mock_data.get_num_records.return_value = 3
        mock_data.get_original_format.return_value = 'format'
        mock_data.get_not_assigned_pct.return_value = 1
        
        data = {
            'name': 'Dataset',
            'user_id': 'test_user',
            'data': mock_data
        }
        
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(
            return_value=MockDatasetManager())
        serializer = DatasetSerializer(data=data)

        serializer.is_valid()
        dataset = serializer.create()

        self.assertDictEqual({
            'name': dataset.name,
            'user_id': dataset.user_id,
            'data': dataset.data,
            'features': dataset.features,
            'label': dataset.label,
            'label_data': dataset.label_data,
            'index_col': dataset.index_col,
            'num_records': dataset.num_records,
            'original_format': dataset.original_format,
            'not_assigned_pct': dataset.not_assigned_pct
        }, {
            'name': data['name'],
            'user_id': data['user_id'],
            'data': [{'foo': 'bar'}],
            'features': ['test_col1', 'test_col2'],
            'label': 'test_label_col',
            'label_data': 'test_label',
            'index_col': 'test_id',
            'num_records': 3,
            'original_format': 'format',
            'not_assigned_pct': 1
        })


    @patch(
        'mlplaygrounds.datasets.serializers.datasets.DatasetSerializer._get_queryset',
        return_value=MagicMock()
    )
    def test_serialize_invalid_data(self, mocked_queryset):
        invalid_data = {
            'name': 'Dataset',
            'user_id': 'testuser',
            'data': {'foo': 'bar'}
        }

        mocked_manager = MockDatasetManager()
        mocked_manager.exists = MagicMock(return_value=True)
        mocked_queryset.return_value = mocked_manager
        
        serializer = DatasetSerializer(data=invalid_data)

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_save_valid_instance(self):
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(return_value=MockSet())
        mocked_serializer.save = MagicMock(
            return_value=Dataset.create(uid=ObjectId()))

        serializer = mocked_serializer()
        saved_dataset = serializer.save(Dataset())

        self.assertIsNotNone(saved_dataset.uid)
    
    def test_save_invalid_instance(self):
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(return_value=MockSet())

        serializer = mocked_serializer()

        with self.assertRaises(TypeError):
            serializer.save(MagicMock())
