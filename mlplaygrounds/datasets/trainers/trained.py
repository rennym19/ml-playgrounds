from sklearn.metrics import mean_squared_error


class TrainedLinearModel:
    def __init__(self, model, features, X_train, X_test, y_train, y_test):
        self.model = model
        self.features = features.to_list()
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def coefficients(self):
        return self.model.coef_.tolist()

    def error(self):
        y_predict = self.model.predict(self.X_test)
        return mean_squared_error(self.y_test, y_predict)
