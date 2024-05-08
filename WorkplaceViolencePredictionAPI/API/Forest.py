import threading
from datetime import time

from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from WorkplaceViolencePredictionAPI.API.models import TrainingData


class Forest:
    _instance = None
    _lock = threading.Lock()  # ensuring singleton is thread-safe

    def __new__(cls):
        """
        Ensures only one instance of the Forest class is created (Singleton pattern).
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, queryset=None):
        """
        Initializes the Forest instance.

        Args:
            queryset (QuerySet): A QuerySet containing training data. Defaults to None,
                in which case it retrieves all TrainingData objects.
        """
        if queryset is None:
            queryset = TrainingData.objects.all().values()
        self.queryset = queryset
        self.dataframe = self.queryset_to_dataframe()
        self.model, self.accuracy = self.create_model()

    def create_model(self):
        """
        Creates and trains a random forest model.

        Returns:
            model (RandomForestClassifier): The trained random forest model.
            accuracy (float): The accuracy of the trained model.
        """
        x = self.dataframe.drop(["id", "createdTime", "wpvRisk"], axis=1)
        y = self.dataframe["wpvRisk"]
        # Splitting the dataset into 70% training and 30% test datasets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
        rf = RandomForestClassifier(n_estimators=100)
        # Training the model on the training dataset
        rf.fit(x_train, y_train)
        # Get test prediction data
        y_pred = rf.predict(x_test)
        return rf, accuracy_score(y_test, y_pred)

    def predict(self, x_test):
        """
        Predicts the workplace violence risk for given test data.

        Args:
            x_test (array-like or sparse matrix): Test data for prediction.

        Returns:
            array-like: Predicted workplace violence risk.
        """
        y_pred = self.model.predict(x_test)
        return y_pred

    def predict_prob(self, x_test):
        """
        Predicts the probabilities of each class for given test data.

        Args:
            x_test (array-like or sparse matrix): Test data for prediction.

        Returns:
            array-like: Predicted probabilities of each class.
        """
        y_pred = self.model.predict_proba(x_test)
        return y_pred

    def queryset_to_dataframe(self) -> DataFrame:
        """
        Converts the queryset to a DataFrame.

        Returns:
            DataFrame: A DataFrame containing the queryset data.
        """
        # pandas doesn't support datetime.time type, so we convert it into milliseconds
        formatted_data = []
        for q in self.queryset:
            time_dt: time = q["timeOfDay"]
            time_ms: float = time_dt.microsecond / 1000
            formatted_data.append({
                'id': q["id"],
                'createdTime': q["createdTime"],
                'avgNurses': q["avgNurses"],
                'avgPatients': q["avgPatients"],
                'percentBedsFull': q["percentBedsFull"],
                'timeOfDay': time_ms,
                'wpvRisk': q["wpvRisk"]
            })
        return DataFrame.from_records(formatted_data)
