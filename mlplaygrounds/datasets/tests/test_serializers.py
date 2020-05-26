from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from django_mock_queries.query import MockModel, MockSet

from bson import ObjectId

from django.contrib.auth import get_user_model

from rest_framework import serializers

from ..db.collections import Dataset
from ..serializers.datasets import DatasetSerializer


class TestDatasetSerializer(TestCase):
    def test_instance_serialization(self):
        instance = MockModel(name='Dataset',
                             user_id='testuser',
                             data={'foo': 'bar', 'inner': {'nested': True}})
        
        serializer = DatasetSerializer(instance)

        self.assertDictEqual(serializer.data, {'uid': None,
                                               'name': instance.name,
                                               'user_id': instance.user_id,
                                               'data': instance.data})
    
    def test_instance_serialization_with_id(self):
        instance = MockModel(uid=ObjectId(),
                             name='Dataset',
                             user_id='testuser',
                             data={'foo': 'bar', 'inner': {'nested': True}})
        
        serializer = DatasetSerializer(instance)

        self.assertDictEqual(serializer.data, {'uid': str(instance.uid),
                                               'name': instance.name,
                                               'user_id': instance.user_id,
                                               'data': instance.data})

    @patch(
        'mlplaygrounds.datasets.serializers.datasets.User',
        return_value=MagicMock()
    )
    def test_serialize_valid_data(self, mocked_user_model):
        data = {
            'name': 'Dataset',
            'user_id': 'testuser',
            'data': {'foo': 'bar', 'inner': {'nested': True}}
        }

        mocked_user_model.objects = MockSet(MockModel(username='testuser'))
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(return_value=MockSet(
            MockModel(name='Another Dataset', user_id='testuser')
        ))
        
        serializer = mocked_serializer(data=data)

        self.assertEqual(serializer.is_valid(), True)

    @patch(
        'mlplaygrounds.datasets.serializers.datasets.User',
        return_value=MagicMock()
    )
    def test_serialize_invalid_data(self, mocked_user_model):
        invalid_data = {
            'name': 'Dataset',
            'user_id': 'testuser',
            'data': {'foo': 'bar'}
        }

        mocked_user_model.objects = MockSet(MockModel(username='testuser'))
        mocked_serializer = DatasetSerializer
        mocked_serializer._get_queryset = MagicMock(return_value=MockSet(
            MockModel(user_id='testuser', name='Dataset')
        ))
        
        serializer = mocked_serializer(data=invalid_data)

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create(self):
        pass

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
