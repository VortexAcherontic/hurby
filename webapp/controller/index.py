from flask import render_template

from twitch_hurby.helix.get_games import get_game_by_id
from twitch_hurby.helix.search_channel import search_channel


def exec_index(hurby):
    streamer_name = hurby.twitch_receiver.twitch_conf.streamer
    channel_data = search_channel(hurby.twitch_receiver.twitch_conf, streamer_name)
    game_data = get_game_by_id(hurby.twitch_receiver.twitch_conf, channel_data["data"][0]["game_id"])
    viewers = len(hurby.char_manager.get_characters())
    data = {
        "is_live": channel_data["data"][0]["is_live"],
        "streamer_name": channel_data["data"][0]["display_name"],
        "stream_title": channel_data["data"][0]["title"],
        "game_title": game_data["data"][0]["name"],
        "viewers": viewers
    }
    return render_template("index.html", botname=hurby.botConfig.botname, data=data)
