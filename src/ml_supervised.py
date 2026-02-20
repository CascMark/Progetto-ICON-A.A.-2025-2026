from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

class SupervisedModels:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.nn_model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=500, random_state=42)
        
        self.rf_accuracy = 0.0
        self.nn_accuracy = 0.0

    def train(self, X_train, y_train, X_test, y_test):
        # 1. Random Forest
        self.rf_model.fit(X_train, y_train)
        preds_rf = self.rf_model.predict(X_test)
        self.rf_accuracy = accuracy_score(y_test, preds_rf)

        # 2. Neural Network
        self.nn_model.fit(X_train, y_train)
        preds_nn = self.nn_model.predict(X_test)
        self.nn_accuracy = accuracy_score(y_test, preds_nn)

        return self.rf_accuracy, self.nn_accuracy

    def predict(self, input_data):
        """
        Restituisce le predizioni di entrambi i modelli e la confidenza del RF.
        """
        # Random Forest
        pred_rf = self.rf_model.predict(input_data)[0]
        prob_rf = max(self.rf_model.predict_proba(input_data)[0])

        # Neural Network
        pred_nn = self.nn_model.predict(input_data)[0]

        return pred_rf, prob_rf, pred_nn