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

router = routers.DefaultRouter()  # routers only work with ViewSets, not regular Views
router.register(r'users', views.UserViewSet)
# for custom ViewSets, we need to explicitly define the basename
router.register(r'hello', views.HelloWorldViewSet, basename='hello')
router.register(r'get_token', views.UserTokenViewSet, basename='token')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/hello_admin/', views.HelloWorldAdmin.as_view(), name='hello-admin')
]
