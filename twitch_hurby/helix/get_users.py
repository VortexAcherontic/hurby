from twitch_hurby.helix import do_bearer_requests


def get_users_by_user_name(users: list, access_token) -> dict:
    url = "https://api.twitch.tv/helix/users?"
    for i in users:
        url = url + "login=" + i + "&"

    return do_bearer_requests.get(url, access_token).json()
