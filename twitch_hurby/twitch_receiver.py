from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.irc.irc_cmd import IRCCommand
from twitch_hurby.irc.irc_connector import IRCConnector
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger
from utils.const import CONST


class TwitchReceiver:
    def __init__(self, hurby):
        self.hurby = hurby
        self.twitch_conf = TwitchConfig(self.hurby)
        self.helix = None
        self.twitch_listener = None
        self.connect_twitch_irc()
        self.connect_twitch_helix()

    def do_command(self, cmd: IRCCommand, char: Character, irc: IRCConnector):
        logger.log(logger.INFO, "Received cmd:\"" + cmd.cmd + "\"")
        logger.log(logger.INFO, "Params:")
        logger.log(logger.INFO, cmd.params)
        twitch_cmds: AbstractCommand = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                tmp: AbstractCommand = twitch_cmds[i]
                if tmp.check_trigger(cmd.cmd):
                    tmp.do_command(None)
        if cmd.cmd == "!whisper":
            logger.log(logger.INFO, "Sending whisper to: " + char)
            irc.send_whisper(char, "Hello: " + char)
        if cmd.cmd == "!users":
            logger.log(logger.INFO, "Checking viewers")
            irc.check_viewers()
        if cmd.cmd == "!shutdown":
            if char.perm == Character.PERM_ADM or char.perm == Character.PERM_MOD:
                CONST.RUNNING = False

    def connect_twitch_helix(self):
        pass
        # self.helix = TwitchHelix(client_id=self.twitch_conf.client_id, oauth_token=self.twitch_conf.oauth_token)

    def connect_twitch_irc(self):
        self.twitch_listener = IRCConnector(self.twitch_conf.bot_username, self.twitch_conf.oauth_token, self, 1,
                                            self.twitch_conf, self.hurby)

    def get_twitch_irc_connector(self) -> IRCConnector:
        return self.twitch_listener
