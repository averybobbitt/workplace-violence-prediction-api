import json
import logging
import os.path
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from WorkplaceViolencePredictionAPI.API.authentication import BearerAuthentication
from WorkplaceViolencePredictionAPI.API.models import HospitalData, TrainingData, IncidentLog, RiskData, EmailRecipient
from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer, TrainingDataSerializer, \
    IncidentDataSerializer, RiskDataSerializer, EmailRecipientSerializer
from WorkplaceViolencePredictionAPI.helpers import risk_to_dict

logger = logging.getLogger("wpv")


# specify no serializer for schema generator
@extend_schema(request=None, responses=None)
class DocumentationView(views.APIView):
    """
    A view to serve the OpenAPI schema for API documentation.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Retrieve and return the OpenAPI schema.
        """
        path = os.path.join(settings.DOCUMENTATION_PATH, "openapi.json")

        try:
            with open(path) as f:
                schema = json.load(f)
        except Exception as e:
            logger.error(f"Error reading OpenAPI schema: {e}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(schema)


class HospitalDataViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for CRUD operations on HospitalData objects.
    """
    queryset = HospitalData.objects.all()
    serializer_class = HospitalDataSerializer
    authentication_classes = [BearerAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def latest(self, request, **kwargs):
        """
        Retrieve the latest HospitalData entry.
        """
        latest_entry = HospitalData.objects.latest()
        serializer = HospitalDataSerializer(latest_entry, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        Create a new HospitalData entry.
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
    """
    A ViewSet for CRUD operations on TrainingData objects.
    """
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer
    authentication_classes = [BearerAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class PredictionModelViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for CRUD operations on PredictionModel objects.
    """
    authentication_classes = [BearerAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RiskData.objects.all()
    serializer_class = RiskDataSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticatedOrReadOnly])
    def latest(self, request, **kwargs):
        """
        Retrieve the latest RiskData entry.
        """
        queryset = RiskData.objects.latest()
        serializer = RiskDataSerializer(queryset, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        Create a new RiskData entry.
        """
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
    """
    A ViewSet for CRUD operations on IncidentLog objects.
    """
    authentication_classes = [BearerAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = IncidentLog.objects.all()
    serializer_class = IncidentDataSerializer

    def create(self, request, **kwargs):
        """
        Create a new IncidentLog entry.
        """
        data = request.data
        required_fields = ["incidentType", "incidentDate", "affectedPeople", "incidentDescription"]

        for field in required_fields:
            if data.get(field) is None:
                return JsonResponse({"error": f"Missing key in body {field}"}, status=status.HTTP_400_BAD_REQUEST)

        incidentType = data.get("incidentType")
        incidentDate = data.get("incidentDate")
        affectedPeople = data.get("affectedPeople")
        incidentDescription = data.get("incidentDescription")

        # find closest HospitalData to incidentDate
        incidentDateTime = datetime.strptime(incidentDate, "%Y-%m-%dT%H:%M")
        closest_hdata = HospitalData.objects.filter(createdTime__lte=incidentDateTime).order_by('-createdTime').first()

        if closest_hdata is None:
            return JsonResponse({"error": f"Couldn't find data prior to given date"}, status=status.HTTP_404_NOT_FOUND)

        new_log = {
            "incidentType": incidentType,
            "incidentDate": incidentDate,
            "affectedPeople": affectedPeople,
            "incidentDescription": incidentDescription,
            "hData": closest_hdata.pk
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
        """
        Delete an IncidentLog entry.
        """
        if row := request.headers.get("id"):
            IncidentLog.objects.get(id=row).delete()
            return JsonResponse({"Success": f"Incident {row} deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            IncidentLog.objects.get(id=row).delete()
            return JsonResponse({"Error": "Missing required id header"}, status=status.HTTP_400_BAD_REQUEST)


class EmailViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for CRUD operations on EmailRecipient objects.
    """
    queryset = EmailRecipient.objects.all()
    serializer_class = EmailRecipientSerializer
    authentication_classes = [BearerAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def send(self, request, **kwargs):
        """
        Send an email to all recipients.
        """
        queryset = EmailRecipient.objects.only("email").values_list("email", flat=True)
        emails = [email for email in queryset]
        logger.debug(queryset)
        logger.debug(emails)

        try:
            # Email sends message to itself and BCCs a list of recipients
            email = EmailMessage(
                subject="Warning: Risk levels in the hospital!",
                body="This message is to inform you of high risk levels within the hospital. "
                     "Please be cautious of heightened stress levels as we work to resolve the issue.",
                bcc=emails,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER]
            )

            email.send()
            return JsonResponse({'message': 'Emails sent successfully'}, status=200)
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return JsonResponse({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List all EmailRecipient objects or retrieve a single object by email.
        """
        # Get query parameter from URL
        email = request.query_params.get('email')

        # If unique_field parameter is present, retrieve single object
        if not email:
            return super().list(request, *args, **kwargs)

        if not isinstance(email, str):
            return JsonResponse({"error": "Email must be a string."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = EmailRecipient.objects.get(email__iexact=email)
            serializer = self.get_serializer(obj)

            return JsonResponse(serializer.data)
        except EmailRecipient.DoesNotExist:
            return JsonResponse({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)


##########################################################


# Home view
@login_required
def home(request):
    """
    Render the home page.
    """
    return render(request, "home.html")


# Log View
@login_required
def log(request):
    """
    Render the log page.
    """
    return render(request, "log.html")


# Manage email View
@login_required
def email(request):
    """
    Render the email management page.
    """
    return render(request, "email.html")


# API documentation View (public)
def docs(request):
    """
    Render the public API documentation page.
    """
    return render(request, "docs.html")
