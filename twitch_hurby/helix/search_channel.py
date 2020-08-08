from twitch_hurby.helix import do_helix_requests
from twitch_hurby.twitch_config import TwitchConfig


def search_channel(twitch_config: TwitchConfig, channel_name: str) -> dict:
    url = "https://api.twitch.tv/helix/search/channels?query=" + channel_name

    return do_helix_requests.get(url, twitch_config).json()


def is_live(twitch_config: TwitchConfig, channel_name: str) -> dict:
    res = search_channel(twitch_config, channel_name)
    return bool(res["data"][0]["is_live"])
