import os


class Const:
    USER_HOME = os.getenv("HOME")
    DEVMODE = False
    DIR_APP_DATA = ".z-ray/hurby"

    if "HURBY_DEVMODE" in os.environ:
        if int(os.environ["HURBY_DEVMODE"]) == 1:
            DIR_APP_DATA = ".z-ray/hurby/dev"
            DEVMODE = True
            print("Running in devmode: "+ str(DEVMODE))

    DIR_APP_DATA_ABSOLUTE = USER_HOME + "/" + DIR_APP_DATA
    DIR_CONF = "config"
    DIR_CHARACTERS = "characters"
    DIR_TMP = "tmp"
    DIR_LOTTERIES_BASE = "lottery"
    DIR_LOTTERIES = "lotteries"

    DIR_TMP_ABSOLUTE = DIR_APP_DATA_ABSOLUTE + "/" + DIR_TMP
    DIR_CONF_ABSOLUTE = DIR_APP_DATA_ABSOLUTE + "/" + DIR_CONF
    DIR_CHARACTERS_ABSOLUTE = DIR_APP_DATA_ABSOLUTE + "/" + DIR_CHARACTERS
    DIR_LOTTERIES_BASE_ABSOLUTE = DIR_CONF_ABSOLUTE + "/" + DIR_LOTTERIES_BASE
    DIR_LOTTERIES_ABSOLUTE = DIR_LOTTERIES_BASE_ABSOLUTE + "/" + DIR_LOTTERIES

    FILE_CONF_HURBY = "hurby_conf.json"
    FILE_CONF_TWITTER = "twitter_conf.json"
    FILE_CONF_PATREON = "patreon_conf.json"
    FILE_CONF_STEAM = "steam_conf.json"
    FILE_CONF_TRELLO = "trello_conf.json"
    FILE_CONF_YOUTUBE = "youtube_conf.json"
    FILE_CONF_TWITCH = "twitch_conf.json"
    FILE_CONF_TWITCH_CMD = "twitch_chat_cmd.json"
    FILE_CONF_LOOTS = "loots_conf.json"
    FILE_CONF_LOTTERY = "lottery_config.json"
    FILE_LOG = "hurby.log"
    FILE_BLACKLIST = "blacklist.json"
    FILE_CHAR_REF_TABLE = "reference_table.json"

    RUNNING = True
    SUPPRESS_JSON_LOGGING = True


CONST = Const()
