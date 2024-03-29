import requests


def hello_world():
    print("hello!")

def get_new_data():
    r = requests.get('api.bobbitt.dev')