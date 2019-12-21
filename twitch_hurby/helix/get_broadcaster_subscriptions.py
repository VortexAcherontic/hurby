from twitch_hurby.helix import do_helix_requests
from twitch_hurby.twitch_config import TwitchConfig


def get_subscriptions(boradcaster_id, twitch_config: TwitchConfig):
    url = "https://api.twitch.tv/helix/subscriptions?broadcaster_id=" + boradcaster_id
    result = do_helix_requests.get(url, twitch_config).json()
    return result
