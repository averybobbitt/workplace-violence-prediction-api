# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HospitalData(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    createdTime = models.DateTimeField(db_column="createdTime", auto_now_add=True, editable=False)
    avgNurses = models.DecimalField(db_column="avgNurses", max_digits=20, decimal_places=10)
    avgPatients = models.DecimalField(db_column="avgPatients", max_digits=20, decimal_places=10)
    percentBedsFull = models.DecimalField(db_column="percentBedsFull", max_digits=20, decimal_places=10)
    timeOfDay = models.TimeField(db_column="timeOfDay")

    class Meta:
        app_label = "API"
        db_table = "hospital_data"
        get_latest_by = ["id"]


class TrainingData(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    createdTime = models.DateTimeField(db_column="createdTime", auto_now_add=True, editable=False)
    avgNurses = models.DecimalField(db_column="avgNurses", max_digits=20, decimal_places=10)
    avgPatients = models.DecimalField(db_column="avgPatients", max_digits=20, decimal_places=10)
    percentBedsFull = models.DecimalField(db_column="percentBedsFull", max_digits=20, decimal_places=10)
    timeOfDay = models.TimeField(db_column="timeOfDay")
    wpvRisk = models.BooleanField(db_column="wpvRisk", default=None)

    class Meta:
        app_label = "API"
        db_table = "training_data"
        get_latest_by = ["id"]


class RiskData(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    hData = models.ForeignKey(HospitalData, null=True, on_delete=models.CASCADE)
    wpvRisk = models.BooleanField(db_column="wpvRisk")
    wpvProbability = models.DecimalField(db_column="wpvProbability", max_digits=3, decimal_places=2)

    class Meta:
        app_label = "API"
        db_table = "risk_data"
        get_latest_by = ["id"]


class IncidentLog(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    incidentType = models.CharField(db_column="incidentType", max_length=255)
    incidentDate = models.DateTimeField(db_column="incidentDate")
    affectedPeople = models.CharField(db_column="affectedPeople", max_length=255)
    incidentDescription = models.CharField(db_column="incidentDescription", max_length=255)
    hData = models.ForeignKey(HospitalData, null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = "API"
        db_table = "incident_log"
        get_latest_by = ["id"]


class EmailRecipient(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(db_column="name", max_length=255)
    email = models.EmailField(db_column="email")

    class Meta:
        app_label = "API"
        db_table = "email_recipient"
        get_latest_by = ["id"]
