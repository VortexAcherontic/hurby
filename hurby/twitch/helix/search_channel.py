from twitch.helix import do_helix_requests
from twitch.twitch_config import TwitchConfig


def search_channel(twitch_config: TwitchConfig, channel_name: str) -> dict:
    url = "https://api.twitch.tv/helix/search/channels?query=" + channel_name
    return do_helix_requests.get(url, twitch_config).json()


def is_live(twitch_config: TwitchConfig, channel_name: str) -> bool:
    res = search_channel(twitch_config, channel_name)
    return bool(res["data"][0]["is_live"])


def get_stream_title(twitch_config: TwitchConfig, channel_name: str) -> str:
    res = search_channel(twitch_config, channel_name)
    return res["data"][0]["title"]


def get_game_id(twitch_config: TwitchConfig, channel_name: str) -> int:
    res = search_channel(twitch_config, channel_name)
    return bool(res["data"][0]["game_id"])
