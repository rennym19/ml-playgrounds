from unittest import TestCase

import pandas as pd

from mlplaygrounds.datasets.trainers.base import Trainer, FeatureTypeError


class TestTrainer(TestCase):
    def setUp(self):
        self.X = [
            {'x_one': 1, 'x_two': 4, 'x_three': 1},
            {'x_one': 2, 'x_two': 6, 'x_three': 1},
            {'x_one': 3, 'x_two': 7, 'x_three': 1},
            {'x_one': 4, 'x_two': None, 'x_three': 1},
            {'x_one': 5, 'x_two': 7, 'x_three': 1}
        ]
        self.y = [5, 8, 10, 9, 12]
        self.exclude_features = ['x_three']
        self.alg = 'linear regression'

        self.trainer = Trainer(self.X, self.y, self.exclude_features, self.alg)

    def test_valid_features_to_exclude(self):
        res = self.trainer.features_to_exclude_are_valid(self.exclude_features)
        
        self.assertEqual(res, True)

    def test_invalid_features_to_exclude(self):
        with self.assertRaises(KeyError):
            self.trainer.features_to_exclude_are_valid(['x_four'])

    def test_valid_algorithm(self):
        res = self.trainer.algorithm_is_valid(self.alg)

        self.assertEqual(res, True)

    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            self.trainer.algorithm_is_valid('invalid_alg')

    def test_valid_features_to_use_at_training(self):
        res = self.trainer.features_to_use_in_training_are_valid()

        self.assertEqual(res, True)

    def test_invalid_features_to_use_at_training(self):
        self.trainer.prepared_X['example'] = ['a', 'b', 'c', 'd', 'e']

        with self.assertRaises(FeatureTypeError):
            self.trainer.features_to_use_in_training_are_valid()

    def test_drop_features(self):
        expected = pd.DataFrame(self.X)
        expected = expected.drop('x_three', axis=1)
        expected = expected.where(pd.notnull(expected), None)        
        expected = expected.to_dict('records')

        self.trainer.drop_features()

        self.assertListEqual(self.get_prepared_X_dict_from_trainer(), expected)
    
    def test_drop_no_features(self):
        self.trainer.exclude_features = []

        self.trainer.drop_features()

        self.assertListEqual(self.get_prepared_X_dict_from_trainer(), self.X)
    
    def test_transform_nan_values(self):
        expected = self.X.copy()
        expected[3]['x_two'] = 6

        self.trainer.transform_nan_values()

        self.assertListEqual(self.get_prepared_X_dict_from_trainer(), expected)

    def test_train(self):
        expected_coef = [0.5, 2.5]

        trained_model = self.trainer.train()
        coefficients = trained_model.coefficients()

        for i, coef in enumerate(expected_coef):
            self.assertAlmostEqual(coefficients[i], coef)

    def get_prepared_X_dict_from_trainer(self):
        prepared_X = self.trainer.prepared_X
        prepared_X = prepared_X.where(pd.notnull(prepared_X), None)
        return prepared_X.to_dict('records')    
