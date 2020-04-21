import requests

from twitch_hurby.helix import validate_token
from utils import logger


def get_bearer_access_token(twitch_config):
    if twitch_config.access_token == "":
        if twitch_config.authorization_code != "":
            _request_bearer_token_first_time(twitch_config)
        else:
            logger.log(logger.ERR, "No authorization code is given, please call the following url in your browser:\n"
                       + _get_auth_code_url(twitch_config) + "\n"
                       + "and put the value of the code= parameter inside the bot config.")
            exit(0)
    elif twitch_config.refresh_token != "":
        if not validate_token.is_token_valid(twitch_config.access_token):
            logger.log(logger.INFO, "Bearer Access token expired, requesting new token pair")
            _refresh_token(twitch_config)
        else:
            logger.log(logger.INFO, "Bearer Access token is valid")
    else:
        logger.log(logger.ERR, "No refresh token given. Please request a new token pair using: "
                   + _get_auth_code_url(twitch_config)
                   + "in your browser and copy the value of code= into the bot authorization_code variable")
        exit(0)


def _request_bearer_token_first_time(twitch_config):
    client_id = twitch_config.client_id
    client_secret = twitch_config.client_secret
    auth_code = twitch_config.authorization_code
    redirect_uri = twitch_config.redirect_url
    url = "https://id.twitch.tv/oauth2/token" \
          "?client_id=" + client_id + \
          "&client_secret=" + client_secret + \
          "&code=" + auth_code + \
          "&grant_type=authorization_code" \
          "&redirect_uri=" + redirect_uri
    response = requests.post(url)
    if response.status_code == 400:
        logger.log(logger.ERR, "Requesting the bearer access token failed, please request a new authorization code.\n"
                   + response.text
                   + _get_auth_code_url(twitch_config))
        exit(0)
    else:
        response_json = response.json()
        twitch_config.access_token = response_json["access_token"]
        twitch_config.refresh_token = response_json["refresh_token"]
        twitch_config.expires_in = response_json["expires_in"]
        twitch_config.authorization_code = ""
        twitch_config.save()


def _refresh_token(twitch_config):
    url = "https://id.twitch.tv/oauth2/token" \
          "?grant_type=refresh_token" \
          "&refresh_token=" + twitch_config.refresh_token + \
          "&client_id=" + twitch_config.client_id + \
          "&client_secret=" + twitch_config.client_secret
    r = requests.post(url)
    if r.status_code == 400:
        logger.log(logger.ERR, "Refreshing the bearer access token failed, please request a new authorization code.\n"
                   + r.text
                   + _get_auth_code_url(twitch_config))
        exit(0)
    else:
        response_json = r.json()
        twitch_config.access_token = response_json["access_token"]
        twitch_config.refresh_token = response_json["refresh_token"]
        twitch_config.expires_in = response_json["expires_in"]
        twitch_config.save()


def _get_auth_code_url(twitch_config):
    return "https://id.twitch.tv/oauth2/authorize" \
           "?client_id=" + twitch_config.client_id + \
           "&redirect_uri=" + twitch_config.redirect_url + \
           "&response_type=code" \
           "&scope=" + twitch_config.twitch_scopes.get_url_scope_request(twitch_config.bot_scopes)
