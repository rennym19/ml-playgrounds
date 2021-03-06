from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from django_mock_queries.query import MockModel, MockSet

from bson import ObjectId

from django.contrib.auth import get_user_model

from rest_framework.serializers import ValidationError

from mlplaygrounds.datasets.db.collections import Dataset, MLModel
from mlplaygrounds.datasets.parsers.parser import ParsedDataset
from mlplaygrounds.datasets.serializers.datasets import DatasetSerializer
from mlplaygrounds.datasets.serializers.models import MLModelLiteSerializer
from ..mocks.managers import MockDatasetManager


class TestDatasetSerializer(TestCase):
    def setUp(self):
        self.valid_instance = MockModel(
            uid=None, name='Dataset', user_id='testuser',
            data={'id': 1, 'foo': 'bar', 'bool': True}, index_col='id',
            label='foo', label_data='bar', num_records=1,
            features=['foo', 'bar'], original_format='csv', not_assigned_pct=0,
            problem_type="classification", y_value_counts=[],
            models=[MLModel.create(name='model', algorithm='test algorithm')]
        )

        instance_dict = dict(self.valid_instance)
        instance_dict['models'] = MLModelLiteSerializer(
            instance_dict['models'], many=True).data

        del instance_dict['save']
        del instance_dict['_MockModel__meta']

        self.expected_valid_instance_data = instance_dict

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
            MockModel(uid=ObjectId(), name='A', user_id='u',
                      data={'a': 'b'}, problem_type='c'),
            MockModel(uid=ObjectId(), name='B', user_id='u',
                      data={'a': 'b'}, problem_type='r')
        ]
        expected_data = [
            {'uid': str(instance.uid),
             'name': instance.name,
             'user_id': instance.user_id,
             'problem_type': instance.problem_type}
            for instance in instances
        ]

        serializer = DatasetSerializer(instances, many=True, exclude_data=True)

        self.assertCountEqual(serializer.data, expected_data)

    def test_serialize_valid_data(self):
        data = {
            'name': 'Dataset',
            'user_id': 'testuser',
            'data': {'foo': 'bar', 'inner': {'nested': True}},
            'problem_type': 'regression'
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
        mock_data.get_y_value_counts.return_value = []
        
        data = {
            'name': 'Dataset',
            'user_id': 'test_user',
            'data': mock_data,
            'problem_type': 'classification'
        }
        
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(
            return_value=MockDatasetManager())
        serializer = DatasetSerializer(data=data)

        serializer.is_valid()
        dataset = serializer.create()

        self.assertDictEqual(dataset.__dict__, {
            'name': data['name'],
            'user_id': data['user_id'],
            'problem_type': data['problem_type'],
            'data': [{'foo': 'bar'}],
            'features': ['test_col1', 'test_col2'],
            'label': 'test_label_col',
            'label_data': 'test_label',
            'index_col': 'test_id',
            'num_records': 3,
            'original_format': 'format',
            'not_assigned_pct': 1,
            'y_value_counts': []
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

        with self.assertRaises(ValidationError):
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
