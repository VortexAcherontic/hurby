from twitch.helix import do_helix_requests
from twitch.twitch_config import TwitchConfig


def is_stream_live(streamer_login: str, twitch_config: TwitchConfig):
    url = "https://api.twitch.tv/helix/streams?user_login=" + streamer_login
    result = do_helix_requests.get(url, twitch_config).json()
    return bool(result["data"])