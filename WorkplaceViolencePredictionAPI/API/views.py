from django.http import JsonResponse
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from WorkplaceViolencePredictionAPI.API.models import HospitalData
from serializers import HospitalDataSerializer

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
class TokenViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tokens = Token.objects.filter(user=request.user)

        if tokens.exists():
            return JsonResponse({'key': tokens[0].key}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)

        if created:
            return JsonResponse({'key': token.key}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'Token already exists'}, status=status.HTTP_400_BAD_REQUEST)


# Hospital data ViewSet
class JsonInputViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalDataSerializer
    queryset = HospitalData.objects.all()

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request, **kwargs):
        serializer = self.get_serializer(self.get_queryset().latest('id'))
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return JsonResponse({'error': 'at least one field is null or an incorrect type'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

