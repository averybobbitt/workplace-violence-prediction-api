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
        fields = ["url", "username", "email", "groups"]


class HospitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalData
        fields = "__all__"
