from os import listdir
from os.path import isfile, join

from twitch_hurby.cmd.cmd_loader import CMDLoader
from utils import logger, json_loader
from utils.const import CONST


class TwitchConfig:
    CMD_PATH = CONST.USER_HOME + "/" + CONST.DIR_APP_DATA + "/templates/commands/twitch/"
    HOST = "irc.twitch.tv"
    PORT = 6667

    def __init__(self, hurby):
        self.hurby = hurby
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_TWITCH
        twitch_json = json_loader.loadJSON(config_file)
        self.onlyfiles = [f for f in listdir(TwitchConfig.CMD_PATH) if isfile(join(TwitchConfig.CMD_PATH, f))]
        self.cmds = [None] * len(self.onlyfiles)
        self.oauth_token = twitch_json["oauth_token"]
        self.channel_name = twitch_json["channel_name"]
        self.streamer = twitch_json["streamer"]
        self.client_id = twitch_json["client_id"]
        self.enable_cron_jobs = twitch_json["enable_cron_jobs"]
        self.cron_job_time = twitch_json["cron_job_time"]
        self.cron_jobs = twitch_json["cron_jobs"]
        self.crawler_time = twitch_json["crawler_time_mins"]
        logger.log(logger.INFO, "Cron jobs: " + str(self.enable_cron_jobs))
        logger.log(logger.INFO, self.cron_jobs)
        self.bot_username = self.hurby.get_bot_config().botname
        self.load_cmds()

    def load_cmds(self):
        cmd_loader = CMDLoader()
        self.cmds = [None] * len(self.onlyfiles)
        for i in range(0, len(self.onlyfiles)):
            cmd_json = json_loader.loadJSON(TwitchConfig.CMD_PATH + self.onlyfiles[i])
            self.cmds[i] = cmd_loader.create_cmd(cmd_json, self.hurby.get_bot_config(), self.hurby)
        logger.log(logger.INFO, str(len(self.cmds)) + " commands loaded")

    def get_cmds(self) -> list:
        return self.cmds
