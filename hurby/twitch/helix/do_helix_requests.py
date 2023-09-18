import requests

from twitch.helix.get_bearer_token import get_bearer_access_token
from twitch.twitch_config import TwitchConfig
from utils import logger


def get(url, twitch_config: TwitchConfig):
    token = twitch_config.access_token
    clientid = twitch_config.client_id
    response = _do_request(url, token, clientid)
    if response.status_code == 401:
        logger.log(logger.WARN, "Twitch Helix request failed for url: " + url
                   + " Message: " + response.text)
        get_bearer_access_token(twitch_config)
        token = twitch_config.access_token
        response = _do_request(url, token, clientid)
        if not (200 <= response.status_code <= 226):
            logger.log(logger.ERR, "Twitch Helix request failed for url: " + url
                       + " Message: " + response.text)
            exit(0)
    return response


def _do_request(url: str, token: str, clientid: str):
    return requests.get(url, headers={"Authorization": "Bearer " + token, "Client-ID": clientid})
