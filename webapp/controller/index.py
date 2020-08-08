from flask import render_template

from twitch_hurby.helix.search_channel import is_live, search_channel


def exec_index(hurby):
    streamer_name = hurby.twitch_receiver.twitch_conf.streamer
    channel_data = search_channel(hurby.twitch_receiver.twitch_conf, streamer_name)
    data = {
        "is_live": channel_data["data"][0]["is_live"],
        "streamer_name": channel_data["data"][0]["display_name"],
        "stream_title": channel_data["data"][0]["title"]
    }
    return render_template("index.html", botname=hurby.botConfig.botname, data=data)
