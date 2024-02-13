from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from WorkplaceViolencePredictionAPI.API.serializers import UserSerializer, GroupSerializer

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
functionality, we can use ViewAPI, as it's a more barebones class which inherits from a Django base class. For more
information, refer to the following links:

https://www.reddit.com/r/django/comments/sm07s2/drf_when_to_use_viewsets_vs_generic_views_vs/
https://stackoverflow.com/questions/41379654/difference-between-apiview-class-and-viewsets-class
https://medium.com/@p0zn/django-apiview-vs-viewsets-which-one-to-choose-c8945e538af4
"""


# ViewSet
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# ViewSet
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Class-based view (not ViewSet!)
class HelloAdmin(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Return a list of all users.
        """
        response = {
            "message": "Hello, admin!",
            "value": 5
        }

        return JsonResponse(response)


# Function-based view
@api_view(["GET"])
def hello(request) -> JsonResponse:
    response = {
        "message": "Hello, world!",
        "value": 5
    }

    return JsonResponse(response)
