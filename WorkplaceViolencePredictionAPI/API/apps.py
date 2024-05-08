import logging
import os

from django.apps import AppConfig

logger = logging.getLogger("wpv")


class ApiConfig(AppConfig):
    """
    Django application configuration for WorkplaceViolencePredictionAPI.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkplaceViolencePredictionAPI.API"

    def ready(self):
        """
        Performs initialization tasks when the application is ready.

        This method is called automatically by Django when the application is initialized.
        """

        # Only run this code if the server is being run
        # (i.e., don't run this if running makemigrations or something)
        if os.environ.get("RUN_MAIN") or os.environ.get("WEB_SERVER_TYPE") == "asgi":
            # Local import to prevent "Apps aren't loaded yet" error
            from WorkplaceViolencePredictionAPI.API.Forest import Forest
            from WorkplaceViolencePredictionAPI.scheduler import updater

            # Create trained model
            logger.info("Creating Forest model...")
            Forest()
            logger.info("Forest model creation complete!")

            # Start background tasks
            logger.info("Starting scheduler...")
            updater.start()
