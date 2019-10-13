from os import listdir
from os.path import isfile, join

from config.bot_config import BotConfig
from twitch_hurby.cmd import cmd_loader, event_loader
from utils import logger, json_loader
from utils.const import CONST


class TwitchConfig:
    CMD_PATH = CONST.DIR_APP_DATA_ABSOLUTE + "/templates/commands/twitch/"
    EVENT_PATH = CONST.DIR_APP_DATA_ABSOLUTE + "/templates/events/twitch/"
    HOST = "irc.twitch.tv"
    PORT = 6667

    def __init__(self, hurby):
        self.hurby = hurby
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_TWITCH
        twitch_json = json_loader.load_json(config_file)
        self.onlyfiles = [f for f in listdir(TwitchConfig.CMD_PATH) if isfile(join(TwitchConfig.CMD_PATH, f))]
        self.cmds = [None] * len(self.onlyfiles)
        self.onlyfiles_events = [f for f in listdir(TwitchConfig.EVENT_PATH) if isfile(join(TwitchConfig.EVENT_PATH, f))]
        self.events = [None] * len(self.onlyfiles_events)
        self.oauth_token = twitch_json["oauth_token"]
        self.channel_name = twitch_json["channel_name"]
        self.streamer = twitch_json["streamer"]
        self.client_id = twitch_json["client_id"]
        self.enable_cron_jobs = twitch_json["enable_cron_jobs"]
        self.cron_job_time = twitch_json["cron_job_time"]
        self.cron_jobs = twitch_json["cron_jobs"]
        self.crawler_time = twitch_json["crawler_time_mins"]
        self.credit_increase_base = twitch_json["credit_increase_base"]
        self.credit_increase_supporter = twitch_json["credit_increase_supporter"]
        self.spend_time = twitch_json["spend_time"]
        logger.log(logger.INFO, "Cron jobs: " + str(self.enable_cron_jobs))
        logger.log(logger.INFO, self.cron_jobs)
        self.bot_username = self.hurby.get_bot_config().botname
        self.load_cmds()
        self.load_events()

    def load_cmds(self):
        self.cmds = [None] * len(self.onlyfiles)
        for i in range(0, len(self.onlyfiles)):
            if self.onlyfiles[i].endswith(".json"):
                cmd_json = json_loader.load_json(TwitchConfig.CMD_PATH + self.onlyfiles[i])
                self.cmds[i] = cmd_loader.create_cmd(cmd_json, self.hurby.get_bot_config(), self.hurby)
        logger.log(logger.INFO, str(len(self.cmds)) + " commands loaded")

    def load_events(self):
        if self.hurby.get_bot_config().modules[BotConfig.MODULE_EVENTS]:
            self.events = [None] * len(self.onlyfiles_events)
            for i in range(0, len(self.onlyfiles_events)):
                if self.onlyfiles_events[i].endswith(".json"):
                    event_json = json_loader.load_json(TwitchConfig.EVENT_PATH + self.onlyfiles_events[i])
                    self.events[i] = event_loader.create_event(event_json, self.hurby.get_bot_config(), self.hurby)

    def get_cmds(self) -> list:
        return self.cmds
