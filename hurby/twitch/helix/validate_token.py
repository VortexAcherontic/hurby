import requests


def is_token_valid(token: str):
    url = "https://id.twitch.tv/oauth2/validate"
    header = {"Authorization": "OAuth " + token}
    r = requests.get(url, headers=header)
    return r.status_code == 200
