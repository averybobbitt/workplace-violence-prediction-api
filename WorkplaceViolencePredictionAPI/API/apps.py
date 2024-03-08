import os

from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from WorkplaceViolencePredictionAPI.API.helpers import queryset_to_dataframe


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkplaceViolencePredictionAPI.API"


# signal function to initialize ML model when the server successfully connects to the database
@receiver(connection_created)
def initialize_ml_model(**kwargs):
    # only run this code if the server is being run (i.e. don't run this if running makemigrations or something)
    if os.environ.get('RUN_MAIN'):
        # local import to prevent "Apps aren't loaded yet" error
        from WorkplaceViolencePredictionAPI.API.models import HospitalData

        # get all current entries
        print("Getting all current HospitalData...")
        queryset = HospitalData.objects.all().values()
        df = queryset_to_dataframe(queryset)
        print(df)
        print("Converting entries to compatible dataframe...")

        print("Training ML model...")
        # forest = create_model(df)
        print("Finished initializing ML model")
