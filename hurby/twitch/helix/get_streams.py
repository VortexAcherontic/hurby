from twitch.helix import do_helix_requests
from twitch.twitch_config import TwitchConfig

_result_size = 100
_stop = 100000


def search_streams_by_game_id(twitch_config: TwitchConfig, game_id) -> list:
    return _build_result(twitch_config, game_id)


def _build_result(twitch_config: TwitchConfig, game_id):
    url = "https://api.twitch.tv/helix/streams?game_id=" + game_id + "&first=" + str(_result_size)
    res = []
    current = do_helix_requests.get(url, twitch_config).json()
    res += current["data"]
    while len(current["data"]) > 0 and len(res) < _stop:
        cursor = current["pagination"]["cursor"]
        current = do_helix_requests.get(url + "&after=" + cursor, twitch_config).json()
        res += current["data"]
    return res
