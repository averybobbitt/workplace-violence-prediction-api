import logging
import os

from django.apps import AppConfig

logger = logging.getLogger("wpv")


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkplaceViolencePredictionAPI.API"

    def ready(self):
        # only run this code if the server is being run (i.e. don't run this if running makemigrations or something)
        if os.environ.get("RUN_MAIN"):
            # local import to prevent "Apps aren't loaded yet" error
            from WorkplaceViolencePredictionAPI.API.Forest import Forest
            from WorkplaceViolencePredictionAPI.scheduler import updater

            # create trained model
            logger.info("Creating Forest model...")
            Forest()
            logger.info("Forest model complete!")

            # start background tasks
            logger.info("Starting scheduler...")
            updater.start()
