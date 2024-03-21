import json
import uuid

from WorkplaceViolencePredictionAPI.API.serializers import HospitalDataSerializer

'''
Takes an array of JSON documents and returns a list of dictionaries for each JSON document.
'''

import json


def json_array_to_dict_list(json_array):
    dict_list = []
    for json_doc in json_array:
        try:
            dict_list.append(json.loads(json_doc))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON document: {e}")
    return dict_list


def populate_db_from_json(dict_list):
    for x in dict_list:

        hospdata = HospitalDataSerializer(id=uuid.uuid4().hex, createdtime=x["createdTime"],
                                          avgnurses=x["avgNurses"], avgpatients=x["avgPatients"],
                                          percentbedsfull=x["percentBedsFull"], timeofday=x["timeOfDay"])
        if hospdata.is_valid():
            hospdata.save()


if __name__ == '__main__':
    with open('sampleData.json', 'r') as f:
        data = json.load(f)
        populate_db_from_json(json_array_to_dict_list(data))