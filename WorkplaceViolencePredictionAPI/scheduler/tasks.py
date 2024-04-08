import logging

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from WorkplaceViolencePredictionAPI.API.models import HospitalData, RiskData
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
    except ValidationError as e:
        # catch exception from invalid input
        logger.error(e)


def predict():
    # get the latest data from hospital data
    queryset = HospitalData.objects.latest()
    riskData_dict = RiskData.dict(None, queryset)
    prediction = riskData_dict.get("wpvRisk")
    probabilities = riskData_dict.get("wpvProbability")

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
    except ValidationError as e:
        # catch exception from invalid input
        logger.error(e)

    # display the risk results
    logger.info({f"Row {queryset.id} is WPV risk": str(prediction),
                 "Probability of WPV": str(probabilities * 100) + "%"})
