import requests


def get_users_by_user_name(users: list, access_token) -> dict:
    url = "https://api.twitch.tv/helix/users?"
    for i in users:
        url = url + "login=" + i + "&"

    r = requests.get(url, headers={"Authorization": "Bearer "+access_token})
    return r.json()
