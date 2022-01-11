import os
import random

from hurby.utils import json_loader
from hurby.utils.const import CONST


class BotConfig:
    MODULE_TWITCH = 0
    MODULE_TWITTER = 1
    MODULE_YOUTUBE = 2
    MODULE_PATREON = 3
    MODULE_STEAM = 4
    MODULE_TRELLO = 5
    MODULE_MINIGAME = 6
    MODULE_EVENTS = 7
    MODULE_WEBSERVER = 8
    MODULE_LOTTERY = 9

    def __init__(self):
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_HURBY
        bot_json = json_loader.load_json(config_file)
        self.botname = bot_json["botname"]
        self.commands_case_sensitive = bot_json["commands_case_sensitive"]
        CONST.SUPPRESS_JSON_LOGGING = bot_json["suppress_json_log"]
        self.modules = [None] * 10
        self.modules[BotConfig.MODULE_TWITCH] = bot_json["modules"]["twitch"]
        self.modules[BotConfig.MODULE_TWITTER] = bot_json["modules"]["twitter"]
        self.modules[BotConfig.MODULE_YOUTUBE] = bot_json["modules"]["youtube"]
        self.modules[BotConfig.MODULE_PATREON] = bot_json["modules"]["patreon"]
        self.modules[BotConfig.MODULE_STEAM] = bot_json["modules"]["steam"]
        self.modules[BotConfig.MODULE_TRELLO] = bot_json["modules"]["trello"]
        self.modules[BotConfig.MODULE_MINIGAME] = bot_json["modules"]["minigame"]
        self.modules[BotConfig.MODULE_EVENTS] = bot_json["modules"]["events"]
        self.modules[BotConfig.MODULE_WEBSERVER] = bot_json["modules"]["webinterface"]
        self.modules[BotConfig.MODULE_LOTTERY] = bot_json["modules"]["lottery"]
        self.bot_name_in_reply = bot_json["bot_name_in_reply"]
        self.unknown_cmd_response = bot_json["unknown_command_response"]
        self.event_cooldown_min_min = bot_json["event"]["cooldown_min_min"]
        self.event_cooldown_max_min = bot_json["event"]["cooldown_max_min"]
        self.respond_on_unknown_command = bot_json["respond_on_unknown_command"]

    def get_unknown_cmd_response(self):
        return self.unknown_cmd_response[random.randint(0, len(self.unknown_cmd_response) - 1)]
