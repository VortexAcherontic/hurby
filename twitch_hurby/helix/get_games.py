from twitch_hurby.helix import do_helix_requests
from twitch_hurby.twitch_config import TwitchConfig


def get_game_by_id(twitch_config: TwitchConfig, game_id) -> dict:
    url = "https://api.twitch.tv/helix/games?id=" + game_id
    return do_helix_requests.get(url, twitch_config).json()


def get_game_by_name(twitch_config: TwitchConfig, game_name: str) -> dict:
    url = "https://api.twitch.tv/helix/games?name=" + game_name
    return do_helix_requests.get(url, twitch_config).json()
