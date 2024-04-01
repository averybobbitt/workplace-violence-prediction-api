import json

import numpy
import pandas as pd
import requests
from django.core.exceptions import ValidationError

from WorkplaceViolencePredictionAPI.API.Forest import Forest
from WorkplaceViolencePredictionAPI.API.models import HospitalData
from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer, RiskDataSerializer


def get_data():
    # request new data from dummy API
    entry = requests.get("https://api.bobbitt.dev/new").json()


    # serialize the new input
    serializer = HospitalDataSerializer(data=entry, many=False)

    try:
        # validate the input
        serializer.is_valid(raise_exception=True)
        # save to the database
        serializer.save()
    except ValidationError:
        # catch exception from invalid input
        print("invalid input")


def predict():
    # get the latest data from hospital data
    queryset = HospitalData.objects.latest()
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

    print({f"Row {queryset.id} is WPV risk": str(prediction),
           "Probability of WPV": str(probabilities * 100) + "%"})
