from unittest import TestCase

from django_mock_queries.query import MockSet, MockModel

from rest_framework.serializers import ValidationError

from ..validators.datasets import (
    validate_dataset_name_type,
    validate_dataset_name_length,
    validate_user_id,
    validate_problem_type
)


class TestDatasetValidators(TestCase):
    def setUp(self):
        pass

    def test_valid_name_length(self):
        self.assertEqual(validate_dataset_name_length('a'*255), 'a'*255)

    def test_invalid_name_length(self):
        with self.assertRaises(ValidationError):
            validate_dataset_name_length('a'*256)

    def test_valid_name_type(self):
        self.assertEqual(validate_dataset_name_type('abc'), 'abc')

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            validate_dataset_name_type(False)
    
    def test_valid_user_id(self):
        qs = MockSet(MockModel(username='test_id'))
        self.assertEqual(validate_user_id(qs, 'test_id'), 'test_id')

    def test_invalid_user_id(self):
        with self.assertRaises(ValidationError):
            validate_user_id(MockSet(), 'test_id')

    def test_valid_problem_type(self):
        self.assertEqual(
            validate_problem_type('classification'), 'classification')
    
    def test_invalid_problem_type(self):
        with self.assertRaises(ValidationError):
            validate_problem_type('notvalid')
