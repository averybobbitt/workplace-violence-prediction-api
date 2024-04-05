import logging

import numpy
import pandas as pd
import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from WorkplaceViolencePredictionAPI.API.Forest import Forest
from WorkplaceViolencePredictionAPI.API.models import HospitalData
from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer, RiskDataSerializer

logger = logging.getLogger("wpv")


def get_data():
    # request new data from dummy API
    entry = requests.get(settings.DATA_SOURCES_NEW).json()

    # serialize the new input
    serializer = HospitalDataSerializer(data=entry, many=False)

    try:
        # validate the input
        serializer.is_valid(raise_exception=True)
        # save to the database
        serializer.save()
        logger.info(f"Saved new data to database: {serializer.data}")
    except ValidationError as e:
        # catch exception from invalid input
        logger.error(e)


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
    logger.info("Making T/F prediction...")

    # make a prediction for the probability
    probabilities = Forest().predict_prob(data_df)[0][1]
    logger.info("Making probability prediction...")

    # prediction is in t/f format, but we have to convert to 0/1 for database
    predictionInt = 1 if prediction else 0

    # create the input json for risk data table
    riskdatainput = {
        "hData": queryset.id,
        "wpvRisk": predictionInt,
        "wpvProbability": probabilities
    }
    # create a serializer for the json input
    serializer = RiskDataSerializer(data=riskdatainput, many=False)

    # if the serializer is valid, save the data to risk data
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Saved risk data to database: {serializer.data}")
    except ValidationError as e:
        # catch exception from invalid input
        logger.error(e)

    # display the risk results
    logger.info({f"Row {queryset.id} is WPV risk": str(prediction),
                 "Probability of WPV": str(probabilities * 100) + "%"})
