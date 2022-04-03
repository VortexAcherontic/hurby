from hurby.twitch.helix import do_helix_requests
from hurby.twitch.twitch_config import TwitchConfig


def get_users_by_user_name(users: list, twitch_config: TwitchConfig) -> dict:
    url = "https://api.twitch.tv/helix/users?"
    for i in users:
        url = url + "login=" + i + "&"

    return do_helix_requests.get(url, twitch_config).json()
