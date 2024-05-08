import numpy
import pandas as pd

from WorkplaceViolencePredictionAPI.API.Forest import Forest


def risk_to_dict(queryset):
    """
    Converts a queryset containing workplace violence risk data into a dictionary containing risk prediction and probability.

    Args:
    - queryset: A queryset containing workplace violence risk data.

    Returns:
    - A dictionary containing the following keys:
        - "hData": ID of the queryset.
        - "wpvRisk": Predicted risk of workplace violence.
        - "wpvProbability": Probability of workplace violence.
    """

    # Extracting features from the queryset
    avgNurses = float(queryset.avgNurses)
    avgPatients = float(queryset.avgPatients)
    percentBedsFull = float(queryset.percentBedsFull)

    # Converting time of day to milliseconds
    timeOfDay = ((queryset.timeOfDay.hour * 3600 + queryset.timeOfDay.minute * 60 + queryset.timeOfDay.second)
                 * 1000 + queryset.timeOfDay.microsecond / 1000)

    # Store data points in a pandas dataframe
    data_df = pd.DataFrame(numpy.array([[avgNurses, avgPatients, percentBedsFull, timeOfDay]]),
                           columns=['avgNurses', 'avgPatients', 'percentBedsFull', 'timeOfDay'])

    # Make a prediction based on the dataframe
    prediction = Forest().predict(data_df)[0]

    # Make a prediction for the probability
    probabilities = Forest().predict_prob(data_df)[0][1]

    return {
        "hData": queryset.id,
        "wpvRisk": prediction,
        "wpvProbability": probabilities
    }
