from hurby.twitch.helix import do_helix_requests
from hurby.twitch.twitch_config import TwitchConfig


def get_subscriptions(boradcaster_id, twitch_config: TwitchConfig):
    url = "https://api.twitch.tv/helix/subscriptions?broadcaster_id=" + boradcaster_id
    result = do_helix_requests.get(url, twitch_config).json()
    return result
