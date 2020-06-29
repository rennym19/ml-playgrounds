from unittest import TestCase
from unittest.mock import patch

from django_mock_queries.query import MockModel

from rest_framework.serializers import ValidationError

from bson import ObjectId

from mlplaygrounds.datasets.db.collections import MLModel
from mlplaygrounds.datasets.serializers.models import MLModelSerializer


class TestMLModelSerializer(TestCase):
    def setUp(self):
        self.valid_instance = MockModel(uid=ObjectId(),
                                        name='test model',
                                        user_id='test_user',
                                        dataset_id=ObjectId(),
                                        algorithm='testalg')
        
        self.data = {
            'uid': str(self.valid_instance.uid),
            'name': self.valid_instance.name,
            'user_id': self.valid_instance.user_id,
            'dataset_id': str(self.valid_instance.dataset_id),
            'algorithm': self.valid_instance.algorithm,
            'features': None,
            'coefficients': None,
            'error': None
        }
    
    def test_serialize_instance(self):
        serialized_data = MLModelSerializer(self.valid_instance).data
        
        self.assertDictEqual(serialized_data, self.data)
    
    def test_serialize_many(self):
        serialized_data = MLModelSerializer([self.valid_instance,
                                             self.valid_instance],
                                            many=True).data
        
        self.assertListEqual(serialized_data, [self.data, self.data])

    @patch.object(MLModelSerializer, 'validate_user_id')
    @patch.object(MLModelSerializer, 'validate_dataset_id')
    def test_validate_data(self, mock_valid_dataset_id, mock_valid_user_id):
        mock_valid_dataset_id.return_value = self.data['dataset_id']
        mock_valid_user_id.return_value = self.data['user_id']

        serializer = MLModelSerializer(data=self.data)

        self.assertEqual(serializer.is_valid(), True)

    def test_validate_invalid_data(self):
        serializer = MLModelSerializer(data={})
        
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    def test_validate_required_field_set(self):
        serializer = MLModelSerializer(data=self.data)

        serializer.validate_field_set(serializer.initial_data, 'name')

    def test_validate_required_field_not_set(self):
        serializer = MLModelSerializer(data={})

        with self.assertRaises(ValidationError):
            serializer.validate_field_set(serializer.initial_data, 'name')

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
        mock_validate_dataset_id.return_value = self.valid_instance.dataset_id
        mock_validate_user_id.return_value = self.data['user_id']
        
        del self.data['uid']

        serializer = MLModelSerializer(data=self.data)
        if serializer.is_valid():
            instance = serializer.create()
            self.assertDictEqual(instance.__dict__, {
                'algorithm': self.valid_instance.algorithm,
                'name': self.valid_instance.name,
                'dataset_id': self.valid_instance.dataset_id,
                'user_id': self.valid_instance.user_id
            })
    
    @patch('mlplaygrounds.datasets.serializers.models.MLModel.objects.update')
    def test_update(self, mock_update):
        mock_update.return_value = 1
        model = MLModel.create(algorithm='SVM', user_id='john', dataset_id=1)
        
        serializer = MLModelSerializer()
        model = serializer.update(model, {'algorithm': 'NN', 'dataset_id': 2})

        self.assertListEqual(
            [model.algorithm, model.dataset_id, model.user_id],
            ['NN', 2, 'john']
        )

    def test_update_field(self):
        model = MockModel(algorithm='NN')

        serializer = MLModelSerializer(model)
        serializer.update_field(model, 'algorithm', 'Logistic Regression')

        self.assertEqual(model.algorithm, 'Logistic Regression')

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
