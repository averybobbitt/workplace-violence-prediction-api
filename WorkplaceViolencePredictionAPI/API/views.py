import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from WorkplaceViolencePredictionAPI.API.models import HospitalData

"""
Django REST framework allows you to combine the logic for a set of related views in a single class, called a ViewSet.
In other frameworks you may also find conceptually similar implementations named something like 'Resources' or
'Controllers'. A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as
.get() or .post(), and instead provides actions such as .list() and .create(). The method handlers for a ViewSet are
only bound to the corresponding actions at the point of finalizing the view, using the .as_view() method. Typically,
rather than explicitly registering the views in a viewset in the urlconf, you'll register the viewset with a router
class, that automatically determines the urlconf for you.

In this project, we will mainly use ViewSets. The primary difference between ViewSet and ViewAPI is the intended use of
the functionality. If the application is performing CRUD actions directly on the model (CREATE, READ, UPDATE, DELETE), 
then ViewSets are better to use. Alternatively, if the application needs finer customization for the requests 
functionality, we can use ViewAPI, as it's a more barebones class which inherits from a Django base View class. For more
information, refer to the following links:

https://www.reddit.com/r/django/comments/sm07s2/drf_when_to_use_viewsets_vs_generic_views_vs/
https://stackoverflow.com/questions/41379654/difference-between-apiview-class-and-viewsets-class
https://medium.com/@p0zn/django-apiview-vs-viewsets-which-one-to-choose-c8945e538af4
"""


# Hello world ViewSet
class HelloViewSet(viewsets.ViewSet):
    @action(detail=False, permission_classes=[permissions.AllowAny])
    def world(self, request):
        return JsonResponse({"message": "Hello, world!"})

    @action(detail=False,
            permission_classes=[permissions.IsAdminUser],
            authentication_classes=[authentication.TokenAuthentication, authentication.BasicAuthentication])
    def admin(self, request):
        return JsonResponse({"message": "Hello, admin!"})


# ViewSet for users to get authentication tokens
class UserTokenViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        username = request.query_params.get('username')
        queryset = User.objects.get(username__iexact=username)
        user = get_object_or_404(queryset)
        token = Token.objects.create(user=user)
        response = {"user": username, "token": token}

        return JsonResponse(response)


# Hospital data ViewSet
class JsonInputViewSet(viewsets.ViewSet):
    def list(self, request):
        row = HospitalData.objects.latest('pid')
        if any([
            row is None,
            row.createdtime is None,
            row.avgnurses is None,
            row.avgpatients is None,
            row.percentbedsfull is None,
            row.timeofday is None
        ]):
            return JsonResponse({})

        if not all([
            isinstance(row.createdtime, datetime.datetime),
            isinstance(row.avgnurses, float),
            isinstance(row.avgpatients, float),
            isinstance(row.percentbedsfull, float),
            isinstance(row.timeofday, datetime.time)

        ]):
            return JsonResponse({})
          
        data = {
            'createdtime': row.createdtime,
            'avgnurses': row.avgnurses,
            'avgpatients': row.avgpatients,
            'percentbedsfull': row.percentbedsfull,
            'timeofday': row.timeofday
        }
        
        return JsonResponse(data)
