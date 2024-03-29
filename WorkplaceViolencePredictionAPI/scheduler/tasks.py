import requests
from django.core.exceptions import ValidationError

from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer


def hello_world():
    print("hello")

def get_data():
    r = requests.get('https://api.bobbitt.dev/new')

    new_entry = requests.get("https://api.bobbitt.dev/new").json()
    serializer = HospitalDataSerializer(data=new_entry, many=False)
    data_size = 1

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("ur good bro")

    except ValidationError:
        print("ur not good bro")