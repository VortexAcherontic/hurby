from twitch_hurby.helix import do_bearer_requests


def get_subscriptions(boradcaster_id, access_token):
    url = "https://api.twitch.tv/helix/subscriptions?broadcaster_id=" + boradcaster_id
    result = do_bearer_requests.get(url, access_token).json()
    return result
