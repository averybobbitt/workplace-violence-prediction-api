from django.db import models


class HospitalData(models.Model):
    """
    Represents data related to hospitals.

    Attributes:
        id (AutoField): Primary key identifying the hospital data.
        createdTime (DateTimeField): Date and time when the data was created (auto-generated).
        avgNurses (DecimalField): Average number of nurses in the hospital.
        avgPatients (DecimalField): Average number of patients in the hospital.
        percentBedsFull (DecimalField): Percentage of hospital beds that are occupied.
        timeOfDay (TimeField): Time of day for which the data is recorded.
    """
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
    """
    Represents training data related to hospitals.

    Attributes:
        id (AutoField): Primary key identifying the training data.
        createdTime (DateTimeField): Date and time when the data was created (auto-generated).
        avgNurses (DecimalField): Average number of nurses in the hospital.
        avgPatients (DecimalField): Average number of patients in the hospital.
        percentBedsFull (DecimalField): Percentage of hospital beds that are occupied.
        timeOfDay (TimeField): Time of day for which the data is recorded.
        wpvRisk (BooleanField): Indicates whether there's a risk of workplace violence.
    """
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
    """
    Represents risk data related to hospitals.

    Attributes:
        id (AutoField): Primary key identifying the risk data.
        hData (ForeignKey): Reference to HospitalData.
        wpvRisk (BooleanField): Indicates whether there's a risk of workplace violence.
        wpvProbability (DecimalField): Probability of workplace violence.
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    hData = models.ForeignKey(HospitalData, null=True, on_delete=models.CASCADE)
    wpvRisk = models.BooleanField(db_column="wpvRisk")
    wpvProbability = models.DecimalField(db_column="wpvProbability", max_digits=3, decimal_places=2)

    class Meta:
        app_label = "API"
        db_table = "risk_data"
        get_latest_by = ["id"]


class IncidentLog(models.Model):
    """
    Represents incident logs related to hospitals.

    Attributes:
        id (AutoField): Primary key identifying the incident log.
        incidentType (CharField): Type of incident.
        incidentDate (DateTimeField): Date and time when the incident occurred.
        affectedPeople (CharField): Description of people affected by the incident.
        incidentDescription (CharField): Description of the incident.
        hData (ForeignKey): Reference to HospitalData.
    """
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
    """
    Represents email recipients.

    Attributes:
        id (AutoField): Primary key identifying the email recipient.
        name (CharField): Name of the recipient.
        email (EmailField): Email address of the recipient (unique).
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(db_column="name", null=True, max_length=255)
    email = models.EmailField(db_column="email", unique=True)

    class Meta:
        app_label = "API"
        db_table = "email_recipient"
        get_latest_by = ["id"]
