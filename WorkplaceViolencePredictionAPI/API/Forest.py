from datetime import time

from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from WorkplaceViolencePredictionAPI.API.models import HospitalData


class Forest:
    def __init__(self):
        # get all current entries
        self.queryset = HospitalData.objects.all().values()
        self.dataframe = self.queryset_to_dataframe()
        self.model = self.create_model()

    # Creates and trains a random forest model
    def create_model(self):
        x = self.dataframe.drop(["id", "createdTime", "wpvRisk"], axis=1)
        y = self.dataframe["wpvRisk"]
        # 70 % training dataset and 30 % test datasets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
        rf = RandomForestClassifier(n_estimators=100)
        # Training the model on the training dataset
        # fit function is used to train the model using the training sets as parameters
        rf.fit(x_train, y_train)
        return rf

    def predict(self, x_test):
        y_pred = self.model.predict(x_test)
        return y_pred

    def predict_prob(self, x_test):
        y_pred = self.model.predict_proba(x_test)
        return y_pred

    def queryset_to_dataframe(self) -> DataFrame:
        # there's probably a better way to do this, but pandas doesn't like the datetime.time type, so we
        # are converting the timeOfDay into an int representing the number of milliseconds that has passed that day
        # (i.e. the timestamp in ms)
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
