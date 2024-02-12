from django.urls import path

from WorkplaceViolencePredictionAPI.api import views

urlpatterns = [
    path("", views.index, name="index"),
]
