import logging
from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.db.models import F, Func
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from WorkplaceViolencePredictionAPI.API.authentication import BearerAuthentication
from WorkplaceViolencePredictionAPI.API.models import HospitalData, TrainingData, IncidentLog, RiskData
from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer, TrainingDataSerializer, \
    IncidentDataSerializer, RiskDataSerializer
from WorkplaceViolencePredictionAPI.helpers import risk_to_dict

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

logger = logging.getLogger("wpv")


class EmailView(generics.GenericAPIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    # send emails to recipients
    def post(self, request):
        try:
            connection = get_connection(
                backend=settings.EMAIL_BACKEND,
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_SENDER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=True
            )

            # Email sends message to itself and BCCs a list of recipients
            email = EmailMessage(
                subject="Warning: Risk levels in the hospital!",
                body="This message is to inform you of high risk levels within the hospital. "
                     "Please be cautious of heightened stress levels as we work to resolve the issue.",
                bcc=settings.EMAIL_RECIPIENTS,
                from_email=settings.EMAIL_HOST_SENDER,
                to=[settings.EMAIL_HOST_SENDER],
                connection=connection,
            )

            email.send()
            return JsonResponse({'message': 'Emails sent successfully'}, status=200)
        except Exception as e:
            logging.error(f"Error sending email: {e}")

    # add an email to the recipients list
    def put(self, request):
        email = request.data.get('email')

        if email is None:
            return JsonResponse({'error': 'Invalid or empty email input'}, status=400)

        settings.EMAIL_RECIPIENTS.append(email)

        return JsonResponse({'message': 'Email appended successfully'}, status=200)

    # remove an email from the recipients list
    def delete(self, request):
        email = request.data.get('email')

        if email is None:
            return JsonResponse({'error': 'Invalid or empty email input'}, status=400)

        settings.EMAIL_RECIPIENTS = [r for r in settings.EMAIL_RECIPIENTS if r != email]

        return JsonResponse({'message': 'Email removed successfully'}, status=200)


# Hospital data ViewSet
class HospitalDataViewSet(viewsets.ModelViewSet):
    queryset = HospitalData.objects.all()
    serializer_class = HospitalDataSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def latest(self, request, **kwargs):
        latest_entry = HospitalData.objects.latest()
        serializer = HospitalDataSerializer(latest_entry, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        This https request is an example for if a hospital uses their own api route to gather their own data
        in a dictionary and want to put it into a database. If a hospital already has a database with
        live information to use, this function is obsolete.
        """

        # walrus operator ( := ) evaluates the expression then assigns the value to the variable
        # (see https://stackoverflow.com/questions/50297704)
        if num_samples := request.headers.get("Samples"):
            # check if num_samples header is an integer greater than 1
            try:
                num_samples = int(num_samples)
                if num_samples < 1:
                    return JsonResponse({"error": "Value must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return JsonResponse({"error": "Value must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

            # if value is good, get N samples
            new_entries = requests.get(f"{settings.DATA_SOURCES_BULK}{num_samples}").json()
            serializer = self.get_serializer(data=new_entries, many=True)
            data_size = len(new_entries)
        else:
            # otherwise, get only 1 sample
            new_entry = requests.get(settings.DATA_SOURCES_NEW).json()
            serializer = self.get_serializer(data=new_entry, many=False)
            data_size = 1
        # save new entry/entries to database
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({"message": f"Successfully added {data_size} entr(y|ies)"},
                                status=status.HTTP_201_CREATED)
        except ValidationError:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainingDataViewSet(viewsets.ModelViewSet):
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class PredictionModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RiskData.objects.all()
    serializer_class = RiskDataSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticatedOrReadOnly])
    def latest(self, request, **kwargs):
        queryset = RiskData.objects.latest()
        serializer = RiskDataSerializer(queryset, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        if row := request.headers.get("id"):
            hData = HospitalData.objects.get(id=row)
        else:
            hData = HospitalData.objects.latest()

        new_entry = risk_to_dict(hData)
        serializer = self.get_serializer(data=new_entry, many=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {f"Row {hData.id} is WPV risk": str(new_entry.get("wpvRisk")),
                        "Probability of WPV": str(new_entry.get('wpvProbability') * 100) + "%"}

            return JsonResponse(response, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentLogViewSet(viewsets.ModelViewSet):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = IncidentLog.objects.all()
    serializer_class = IncidentDataSerializer

    def create(self, request, **kwargs):
        headers = request.headers
        req_headers = ["incidentType", "incidentDate", "affectedPeople", "incidentDescription"]
        for header in req_headers:
            if headers.get(header) is None:
                return JsonResponse({"error": f"Missing header {header}"}, status=status.HTTP_400_BAD_REQUEST)
        closest_hdata = (HospitalData.objects.annotate(
            time_difference=Func(F("createdTime") - datetime.strptime(headers.get("incidentDate"), "%Y-%m-%d %H:%M:%S"),
                                 function="ABS"))
                         .order_by("time_difference").first().id)
        new_log = {
            "incidentType": headers.get("incidentType"),
            "incidentDate": headers.get("incidentDate"),
            "affectedPeople": headers.get("affectedPeople"),
            "incidentDescription": headers.get("incidentDescription"),
            "hData": closest_hdata
        }
        serializer = self.serializer_class(data=new_log, many=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({"Status": f"Incident {serializer.data.get('id')} logged"},
                                status=status.HTTP_201_CREATED)
        except ValidationError:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        if row := request.headers.get("id"):
            IncidentLog.objects.get(id=row).delete()
            return JsonResponse({"Success": f"Incident {row} deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            IncidentLog.objects.get(id=row).delete()
            return JsonResponse({"Error": "Missing required id header"}, status=status.HTTP_400_BAD_REQUEST)


##########################################################


# Home view
def home(request):
    return render(request, "home.html")


# Log View
def log(request):
    return render(request, "incidentlog.html")


# Manage email View
def email(request):
    return render(request, "email.html")


# API documentation View
def docs(request):
    return render(request, "docs.html")
