import os


class _Const:
    USER_HOME = os.getenv("HOME")

    DIR_APP_DATA = ".z-ray/hurby"
    DIR_CONF = "config"
    DIR_CONF_ABSOLUTE = USER_HOME + "/" + DIR_APP_DATA + "/" + DIR_CONF

    FILE_CONF_HURBY = "hurby_conf.json"
    FILE_CONF_TWITTER = "twitter_conf.json"
    FILE_CONF_PATREON = "patreon_conf.json"
    FILE_CONF_STEAM = "steam_conf.json"
    FILE_CONF_TRELLO = "trello_conf.json"
    FILE_CONF_YOUTUBE = "youtube_conf.json"
    FILE_CONF_TWITCH = "twitch_conf.json"
    FILE_CONF_TWITCH_CMD = "twitch_chat_cmd.json"
    FILE_LOG = "hurby.log"


CONST = _Const()
