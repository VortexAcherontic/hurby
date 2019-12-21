import requests

from twitch_hurby.helix.get_bearer_token import get_bearer_access_token
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger


def get(url, twitch_config: TwitchConfig):
    token = twitch_config.access_token
    response = _do_request(url, token)
    if response.status_code == 401:
        logger.log(logger.WARN,
                   "Twitch Helix request failed for url: " + url + " Message: " + response.text + " token: " + token)
        get_bearer_access_token(twitch_config)
        token = twitch_config.access_token
        response = _do_request(url, token)
        if not (200 <= response.status_code <= 226):
            logger.log(logger.ERR,
                       "Twitch Helix request failed for url: " + url + " Message: " + response.text + " token: " + token)
            exit(0)
    return response


def _do_request(url: str, token: str):
    return requests.get(url, headers={"Authorization": "Bearer " + token})
