import os

from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from WorkplaceViolencePredictionAPI.API.helpers import queryset_to_dataframe, create_model

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkplaceViolencePredictionAPI.API"

# signal function to initialize ML model when the server successfully connects to the database
@receiver(connection_created)
def initialize_ml_model(**kwargs):
    global forest
    # only run this code if the server is being run (i.e. don't run this if running makemigrations or something)
    if os.environ.get("RUN_MAIN"):
        # local import to prevent "Apps aren't loaded yet" error
        from WorkplaceViolencePredictionAPI.API.models import HospitalData

        # get all current entries
        queryset = HospitalData.objects.all().values()
        # convert QuerySet to DataFrame
        df = queryset_to_dataframe(queryset)
        forest = create_model(df)
def get_forest():
    return forest