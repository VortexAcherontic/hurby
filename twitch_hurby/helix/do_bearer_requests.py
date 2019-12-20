import requests

from utils import logger


def get(url, token):
    response = requests.get(url, headers={"Authorization": "Bearer " + token})
    if response.status_code == 401:
        logger.log(logger.ERR,
                   "Twitch Helix request failed for url: " + url + " Message: " + response.text + " token: " + token)
    return response
