from django.db import models

class HospModel(models.Model):
    pid = models.UUIDField
    timestamp = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField()
    staffing = models.IntegerField()
    patients = models.IntegerField()
