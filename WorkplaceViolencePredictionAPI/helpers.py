import numpy
import pandas as pd

from WorkplaceViolencePredictionAPI.API.Forest import Forest


def risk_to_dict(queryset):
    avgNurses = float(queryset.avgNurses)
    avgPatients = float(queryset.avgPatients)
    percentBedsFull = float(queryset.percentBedsFull)
    timeOfDay = ((queryset.timeOfDay.hour * 3600 + queryset.timeOfDay.minute * 60 + queryset.timeOfDay.second)
                 * 1000 + queryset.timeOfDay.microsecond / 1000)

    # store data points in a pandas dataframe
    data_df = pd.DataFrame(numpy.array([[avgNurses, avgPatients, percentBedsFull, timeOfDay]]),
                           columns=['avgNurses', 'avgPatients', 'percentBedsFull', 'timeOfDay'])

    # make a prediction based on the dataframe
    prediction = Forest().predict(data_df)[0]

    # make a prediction for the probability
    probabilities = Forest().predict_prob(data_df)[0][1]

    return {
        "hData": queryset.id,
        "wpvRisk": prediction,
        "wpvProbability": probabilities
    }
