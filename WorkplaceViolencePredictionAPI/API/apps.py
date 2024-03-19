import os

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkplaceViolencePredictionAPI.API"

    def ready(self):
        # only run this code if the server is being run (i.e. don't run this if running makemigrations or something)
        if os.environ.get("RUN_MAIN"):
            # local import to prevent "Apps aren't loaded yet" error
            from WorkplaceViolencePredictionAPI.API.Forest import Forest

            # create trained model
            Forest()
