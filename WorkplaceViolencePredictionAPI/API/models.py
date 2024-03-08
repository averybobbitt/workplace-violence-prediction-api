# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HospitalData(models.Model):
    id = models.SmallAutoField(primary_key=True, editable=False)
    createdtime = models.DateTimeField(db_column='createdTime', auto_now_add=True, editable=False)
    avgnurses = models.DecimalField(db_column='avgNurses', max_digits=20, decimal_places=10)
    avgpatients = models.DecimalField(db_column='avgPatients', max_digits=20, decimal_places=10)
    percentbedsfull = models.DecimalField(db_column='percentBedsFull', max_digits=20, decimal_places=10)
    timeofday = models.TimeField(db_column='timeOfDay')
    wpvrisk = models.BooleanField(db_column='wpvRisk', default=None)

    class Meta:
        app_label = 'API'
        db_table = 'hospital_data'
        get_latest_by = ['id']
