from unittest import TestCase
from unittest.mock import patch

from django_mock_queries.query import MockModel

from rest_framework.serializers import ValidationError

from bson import ObjectId

from mlplaygrounds.datasets.serializers.models import MLModelSerializer


class TestMLModelSerializer(TestCase):
    def setUp(self):
        self.valid_instance = MockModel(uid=ObjectId(),
                                        name='test model',
                                        user_id='test_user',
                                        dataset_id='test_dataset',
                                        algorithm='testalg')
        
        self.data = {
            'uid': str(self.valid_instance.uid),
            'name': self.valid_instance.name,
            'user_id': self.valid_instance.user_id,
            'dataset_id': self.valid_instance.dataset_id,
            'algorithm': self.valid_instance.algorithm,
        }
    
    def test_serialize_instance(self):
        serialized_data = MLModelSerializer(self.valid_instance).data
        
        self.assertDictEqual(serialized_data, self.data)
    
    def test_serialize_many(self):
        serialized_data = MLModelSerializer([self.valid_instance,
                                             self.valid_instance],
                                            many=True).data
        
        self.assertListEqual(serialized_data, [self.data, self.data])
    
    @patch.object(MLModelSerializer, 'validate_dataset_id')
    @patch.object(MLModelSerializer, 'validate_user_id')
    def test_validate_data(self, mock_valid_dataset_id, mock_valid_user_id):
        mock_valid_dataset_id.return_value = self.data['dataset_id']
        mock_valid_user_id.return_value = self.data['user_id']

        serializer = MLModelSerializer(data=self.data)

        self.assertEqual(serializer.is_valid(), True)

    def test_validate_invalid_data(self):
        serializer = MLModelSerializer(data={})
        
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    @patch('mlplaygrounds.datasets.serializers.models.User.objects')
    def test_validate_invalid_user_id(self, mock_query):
        mock_query.filter.return_value = mock_query
        mock_query.exists.return_value = False

        serializer = MLModelSerializer()

        with self.assertRaises(ValidationError):
            serializer.validate_user_id('invalid')
    
    @patch('mlplaygrounds.datasets.serializers.models.Dataset.objects')
    def test_validate_non_existant_dataset_id(self, mock_query):
        mock_query.exists.return_value = False

        serializer = MLModelSerializer()

        with self.assertRaises(ValidationError):
            serializer.validate_dataset_id('invalid')

    def test_validate_invalid_type_id(self):
        serializer = MLModelSerializer()

        with self.assertRaises(ValidationError):
            serializer.validate_dataset_id(0)
    
    def test_validate_invalid_id(self):
        serializer = MLModelSerializer()

        with self.assertRaises(ValidationError):
            serializer.validate_dataset_id('invalid')

    @patch.object(MLModelSerializer, 'validate_user_id')
    @patch.object(MLModelSerializer, 'validate_dataset_id')
    def test_create(self, mock_validate_dataset_id, mock_validate_user_id):
        mock_validate_dataset_id.return_value = self.data['dataset_id']
        mock_validate_user_id.return_value = self.data['user_id']
        
        del self.data['uid']

        serializer = MLModelSerializer(data=self.data)
        if serializer.is_valid():
            instance = serializer.create()
            self.assertDictEqual(instance.__dict__, self.data)

    @patch('mlplaygrounds.datasets.serializers.models.MLModel.objects.save') 
    @patch('mlplaygrounds.datasets.serializers.models.isinstance')
    def test_save(self, mock_is_instance, mock_save):
        mock_is_instance.return_value = True
        mock_save.return_value = MockModel(uid=ObjectId())

        serializer = MLModelSerializer()
        saved_instance = serializer.save(MockModel())

        self.assertIsNotNone(saved_instance.uid)
    
    def test_save_invalid_instance(self):
        serializer = MLModelSerializer()
        
        with self.assertRaises(TypeError):
            serializer.save(MockModel())