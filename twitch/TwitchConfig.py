from os import listdir
from os.path import isfile, join

from twitch.cmd.CMDLoader import CMDLoader
from utils import Logger, JSONLoader
from utils.Const import CONST


class TwitchConfig:
    CMD_PATH = CONST.USER_HOME + "/" + CONST.DIR_APP_DATA + "/templates/commands/twitch/"

    def __init__(self, hurby):
        self.hurby = hurby
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_TWITCH
        twitch_json = JSONLoader.loadJSON(config_file)
        self.onlyfiles = [f for f in listdir(TwitchConfig.CMD_PATH) if isfile(join(TwitchConfig.CMD_PATH, f))]
        self.cmds = [None] * len(self.onlyfiles)
        self.load_cmds()
        self.oauth_token = twitch_json["oauth_token"]
        self.channel_name = twitch_json["channel_name"]
        self.client_id = twitch_json["client_id"]
        self.bot_username = self.hurby.botConfig.botname

    def load_cmds(self):
        cmd_loader = CMDLoader()
        self.cmds = [None] * len(self.onlyfiles)
        for i in range(0, len(self.onlyfiles)):
            cmd_json = JSONLoader.loadJSON(TwitchConfig.CMD_PATH + self.onlyfiles[i])
            self.cmds[i] = cmd_loader.create_cmd(cmd_json, self.bot_config)
        Logger.log(Logger.INFO, str(len(self.cmds)) + " commands loaded")

    def get_cmds(self):
        return self.cmds
