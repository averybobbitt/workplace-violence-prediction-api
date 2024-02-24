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
