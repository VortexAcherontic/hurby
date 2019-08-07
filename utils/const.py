import os
import sys

from utils import logger


class Const:
    USER_HOME = os.getenv("HOME")

    if len(sys.argv) > 0:
        if sys.argv[1] == "dev":
            logger.log(logger.INFO, "CONST: Enable dev mode FS")
            DIR_APP_DATA = ".z-ray/hurby/dev"
    else:
        DIR_APP_DATA = ".z-ray/hurby"

    DIR_APP_DATA_ABSOLUTE = USER_HOME + "/" + DIR_APP_DATA
    DIR_CONF = "config"
    DIR_CHARACTERS = "characters"
    DIR_CONF_ABSOLUTE = DIR_APP_DATA_ABSOLUTE + "/" + DIR_CONF
    DIR_CHARACTERS_ABSOLUTE = DIR_APP_DATA_ABSOLUTE + "/" + DIR_CHARACTERS

    FILE_CONF_HURBY = "hurby_conf.json"
    FILE_CONF_TWITTER = "twitter_conf.json"
    FILE_CONF_PATREON = "patreon_conf.json"
    FILE_CONF_STEAM = "steam_conf.json"
    FILE_CONF_TRELLO = "trello_conf.json"
    FILE_CONF_YOUTUBE = "youtube_conf.json"
    FILE_CONF_TWITCH = "twitch_conf.json"
    FILE_CONF_TWITCH_CMD = "twitch_chat_cmd.json"
    FILE_LOG = "hurby.log"
    FILE_BLACKLIST = "blacklist.json"
    FILE_CHAR_REF_TABLE = "reference_table.json"

    RUNNING = True


CONST = Const()
