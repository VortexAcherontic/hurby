import requests


def get(url, token):
    return requests.get(url, headers={"Authorization": "Bearer " + token})
