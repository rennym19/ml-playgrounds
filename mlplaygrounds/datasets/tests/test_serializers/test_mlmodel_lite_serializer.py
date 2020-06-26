from unittest import TestCase
from unittest.mock import patch

from django_mock_queries.query import MockModel

from bson import ObjectId

from mlplaygrounds.datasets.serializers.models import MLModelLiteSerializer


class TestMLModelLiteSerializer(TestCase):
    def setUp(self):
        self.valid_instance = MockModel(uid=ObjectId(),
                                        name='test model',
                                        user_id='test_user',
                                        dataset_id='test_dataset',
                                        algorithm='testalg')
        
        self.expected_data = {
            'uid': str(self.valid_instance.uid),
            'name': self.valid_instance.name,
            'algorithm': self.valid_instance.algorithm,
        }
    
    def test_serialize_instance(self):
        serialized_data = MLModelLiteSerializer(self.valid_instance).data
        self.assertDictEqual(serialized_data, self.expected_data)
    
    def test_serialize_many(self):
        expected_list = [self.expected_data, self.expected_data]

        serialized_data = MLModelLiteSerializer(
            [self.valid_instance, self.valid_instance], many=True).data
        
        self.assertListEqual(serialized_data, expected_list)
