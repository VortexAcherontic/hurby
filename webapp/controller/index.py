from flask import render_template

from twitch_hurby.helix.get_games import get_game_by_id
from twitch_hurby.helix.get_streams import search_streams_by_game_id
from twitch_hurby.helix.search_channel import search_channel


def exec_index(hurby):
    twitch_conf = hurby.twitch_receiver.twitch_conf
    streamer_name = twitch_conf.streamer
    channel_data = search_channel(twitch_conf, streamer_name)
    game_id = channel_data["data"][0]["game_id"]
    game_data = get_game_by_id(twitch_conf, game_id)
    viewers = len(hurby.char_manager.get_characters())
    stream_by_game = search_streams_by_game_id(twitch_conf, game_id)
    data = {
        "is_live": channel_data["data"][0]["is_live"],
        "streamer_name": channel_data["data"][0]["display_name"],
        "stream_title": channel_data["data"][0]["title"],
        "game_title": game_data["data"][0]["name"],
        "viewers": viewers,
        "other_streams": len(stream_by_game)
    }
    return render_template("index.html", botname=hurby.botConfig.botname, data=data)
