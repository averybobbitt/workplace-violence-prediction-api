"""
URL configuration for WorkplaceViolencePredictionAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from WorkplaceViolencePredictionAPI.API import views

# routers only work with ViewSets, not regular Views
# for ViewSets not associated with a model, we need to explicitly define the basename
router = routers.DefaultRouter()
router.register(r"hello", views.HelloViewSet, basename="hello")
router.register(r"token", views.TokenViewSet, basename="token")
router.register(r"data", views.HospitalDataViewSet)
router.register(r"model", views.PredictionModelViewSet, basename="model")
router.register(r"email", views.EmailViewSet, basename="email")
router.register(r"log", views.IncidentLogViewSet)
router.register(r"train", views.TrainingDataViewSet)
router.register(r"bruh", views.BruhViewSet)

urlpatterns = [
    path("", views.home),
    path("log/", views.log),
    path("email/", views.manage_emails),
    path("admin/", admin.site.urls),  # built-in admin portal for Django
    path("api/", include(router.urls)),  # router paths defined above
    path("api/auth/", include("rest_framework.urls")),  # login/out for browser view
]
