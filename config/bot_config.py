import random
import sys

from utils import json_loader, logger
from utils.const import CONST


class BotConfig:
    MODULE_TWITCH = 0
    MODULE_TWITTER = 1
    MODULE_YOUTUBE = 2
    MODULE_PATREON = 3
    MODULE_STEAM = 4
    MODULE_TRELLO = 5
    MODULE_MINIGAME = 6

    def __init__(self):
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_HURBY
        bot_json = json_loader.loadJSON(config_file)
        self.botname = bot_json["botname"]
        self.modules = [None] * 7
        self.modules[BotConfig.MODULE_TWITCH] = bot_json["modules"]["twitch"]
        self.modules[BotConfig.MODULE_TWITTER] = bot_json["modules"]["twitter"]
        self.modules[BotConfig.MODULE_YOUTUBE] = bot_json["modules"]["youtube"]
        self.modules[BotConfig.MODULE_PATREON] = bot_json["modules"]["patreon"]
        self.modules[BotConfig.MODULE_STEAM] = bot_json["modules"]["steam"]
        self.modules[BotConfig.MODULE_TRELLO] = bot_json["modules"]["trello"]
        self.modules[BotConfig.MODULE_MINIGAME] = bot_json["modules"]["minigame"]
        self.bot_name_in_reply = bot_json["bot_name_in_reply"]
        self.unknown_cmd_response = bot_json["unknown_command_response"]
        self.dev_mode = False
        if len(sys.argv) > 0:
            if sys.argv[1] == "dev":
                logger.log(logger.INFO, "BotConfig: Enable devmode")
                self.dev_mode = True

    def get_unknown_cmd_response(self):
        return self.unknown_cmd_response[random.randint(0, len(self.unknown_cmd_response) - 1)]
