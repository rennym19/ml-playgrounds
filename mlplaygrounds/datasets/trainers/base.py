import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split

from .trained import TrainedLinearModel


VALID_ALGORITHMS = ['linear regression']
# 'logistic regression', 'svm', 'decission tree', 'random forests'


class Trainer:
    def __init__(self, X, y, exclude_features, algorithm):
        self.X = pd.DataFrame(X)
        self.y = y

        if self.features_to_exclude_are_valid(exclude_features):
            self.exclude_features = exclude_features

        self.algorithm = algorithm

        self.prepared_X = self.X
    
    def features_to_exclude_are_valid(self, features):
        valid_features = self.X.columns
        for feature in features:
            if feature not in valid_features:
                raise KeyError(f'"{feature}" is not a feature')
        return True
    
    def train(self):
        if self.algorithm_is_valid(self.algorithm):
            self.drop_features()
            self.transform_nan_values()

            if self.features_to_use_in_training_are_valid():
                X_train, X_test, y_train, y_test = train_test_split(
                    self.prepared_X, self.y, random_state=0)

                model = self.fit_data(X_train, y_train)
                return TrainedLinearModel(model, self.prepared_X.columns,
                                          X_train, X_test, y_train, y_test)

    def fit_data(self, X_train, y_train):
        if self.algorithm == VALID_ALGORITHMS[0]:
            reg = linear_model.LinearRegression()
            reg.fit(X_train, y_train)
            return reg
        raise ValueError(f'{self.algorithm} is not valid/supported')
            
    def algorithm_is_valid(self, algorithm):
        if algorithm not in VALID_ALGORITHMS:
            raise ValueError(f'{algorithm} is not a valid/supported algorithm')
        return True
    
    def features_to_use_in_training_are_valid(self):
        features = self.prepared_X.columns
        for feature in features:
            if not np.issubdtype(self.prepared_X[feature].dtype, np.number):
                raise FeatureTypeError(f'{feature} is not a numeric feature. '
                                        'It cannot be used for training.')
        return True

    def drop_features(self):
        self.prepared_X.drop(self.exclude_features, axis=1, inplace=True)
    
    def transform_nan_values(self):
        for feature in self.prepared_X.columns:
            feature_mean = self.prepared_X[feature].mean()
            self.prepared_X[feature].fillna(feature_mean, inplace=True)


class FeatureTypeError(Exception):
    pass
