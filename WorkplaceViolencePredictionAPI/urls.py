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
from rest_framework.authtoken.views import obtain_auth_token

from WorkplaceViolencePredictionAPI.API import views

# routers only work with ViewSets, not regular Views
# for ViewSets not associated with a model, we need to explicitly define the basename
router = routers.DefaultRouter()
router.register(r"data", views.HospitalDataViewSet)
router.register(r"train", views.TrainingDataViewSet)
router.register(r"model", views.PredictionModelViewSet)
router.register(r"log", views.IncidentLogViewSet)

email_urls = [
    path("send/", views.EmailView.as_view()),
    path("append/", views.EmailView.as_view()),
    path("remove/", views.EmailView.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),  # built-in admin portal for Django
    # Webpage Routes
    path("", views.home, name="home"),
    path("log/", views.log, name="log"),
    path("email/", views.manage_emails, name="email"),
    # API Routes
    path("api/", include(router.urls)),  # router paths defined above
    path("api/auth/", include("rest_framework.urls")),  # login/out for browser view
    path("api/token/", obtain_auth_token),
    path("api/email/", include(email_urls)),
]
