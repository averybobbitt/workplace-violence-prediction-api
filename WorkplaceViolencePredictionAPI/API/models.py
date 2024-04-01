# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HospitalData(models.Model):
    id = models.SmallAutoField(primary_key=True)
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    avgNurses = models.DecimalField(db_column='avgNurses', max_digits=20, decimal_places=10)  # Field name made lowercase.
    avgPatients = models.DecimalField(db_column='avgPatients', max_digits=20, decimal_places=10)  # Field name made lowercase.
    percentBedsFull = models.DecimalField(db_column='percentBedsFull', max_digits=20, decimal_places=10)  # Field name made lowercase.
    timeOfDay = models.TimeField(db_column='timeOfDay')  # Field name made lowercase.

    class Meta:
        app_label = "API"
        db_table = 'hospital_data'
        get_latest_by = ["id"]
        
class TrainingData(models.Model):
    id = models.SmallAutoField(primary_key=True)
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    avgNurses = models.DecimalField(db_column='avgNurses', max_digits=20, decimal_places=10)  # Field name made lowercase.
    avgPatients = models.DecimalField(db_column='avgPatients', max_digits=20, decimal_places=10)  # Field name made lowercase.
    percentBedsFull = models.DecimalField(db_column='percentBedsFull', max_digits=20, decimal_places=10)  # Field name made lowercase.
    timeOfDay = models.TimeField(db_column='timeOfDay')  # Field name made lowercase.
    wpvRisk = models.IntegerField(db_column='wpvRisk')  # Field name made lowercase.

    class Meta:
        app_label = "API"
        db_table = 'training_data'
        get_latest_by = ["id"]

class RiskData(models.Model):
    id = models.SmallAutoField(primary_key=True)
    hdata = models.ForeignKey(HospitalData, models.DO_NOTHING, db_column='hData_id')  # Field name made lowercase.
    wpvrisk = models.TextField(db_column='wpvRisk')  # Field name made lowercase. This field type is a guess.
    wpvprobability = models.DecimalField(db_column='wpvProbability', max_digits=3, decimal_places=2)  # Field name made lowercase.

    class Meta:
        app_label = "API"
        db_table = 'risk_data'
        get_latest_by = ["id"]

class IncidentLog(models.Model):
    id = models.SmallAutoField(primary_key=True)
    incidenttype = models.CharField(db_column='incidentType', max_length=255)  # Field name made lowercase.
    incidentdate = models.DateTimeField(db_column='incidentDate')  # Field name made lowercase.
    affectedpeople = models.CharField(db_column='affectedPeople', max_length=255, blank=True, null=True)  # Field name made lowercase.
    incidentdescription = models.CharField(db_column='incidentDescription', max_length=255)  # Field name made lowercase.
    hdata = models.ForeignKey('TrainingData', models.DO_NOTHING, db_column='hData_id')  # Field name made lowercase.

    class Meta:
        app_label = "API"
        db_table = 'incident_log'
        get_latest_by = ["id"]

