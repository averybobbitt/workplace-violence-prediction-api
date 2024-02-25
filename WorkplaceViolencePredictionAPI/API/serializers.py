import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from WorkplaceViolencePredictionAPI.API.models import HospitalData

"""
Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can
then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed
data to be converted back into complex types, after first validating the incoming data. The serializers in REST
framework work very similarly to Django's Form and ModelForm classes. We provide a Serializer class which gives you a 
powerful, generic way to control the output of your responses, as well as a ModelSerializer class which provides a 
useful shortcut for creating serializers that deal with model instances and querysets.
"""


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class HospitalDataSerializer(serializers.ModelSerializer):
    id = serializers.CharField(primary_key=True, max_length=36)
    createdtime = serializers.DateTimeField(db_column='createdTime')
    avgnurses = serializers.DecimalField(db_column='avgNurses', max_digits=10, decimal_places=0)
    avgpatients = serializers.DecimalField(db_column='avgPatients', max_digits=10, decimal_places=0)
    percentbedsfull = serializers.DecimalField(db_column='percentBedsFull', max_digits=10, decimal_places=0)
    timeofday = serializers.TimeField(db_column='timeOfDay')

    class Meta:
        model = HospitalData
        fields = ['id', 'createdtime', 'avgnurses', 'avgpatients', 'percentbedsfull', 'timeofday']

    def validate(self, data):
        if any([
            data.id is None,
            data.createdtime is None,
            data.avgnurses is None,
            data.avgpatients is None,
            data.percentbedsfull is None,
            data.timeofday is None
        ]):
            raise serializers.ValidationError("At least one field is null")

        if not all([
            isinstance(data.createdtime, datetime.datetime),
            isinstance(data.avgnurses, float),
            isinstance(data.avgpatients, float),
            isinstance(data.percentbedsfull, float),
            isinstance(data.timeofday, datetime.time)
        ]):
            raise serializers.ValidationError("Some data is of the wrong type")

        return data
