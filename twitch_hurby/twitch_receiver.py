from character.character import Character
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
        twitch_cmds = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                # logger.log(logger.INFO, "Checking: "+twitch_cmds[i].cmd)
                if cmd.cmd == twitch_cmds[i].cmd:
                    if twitch_cmds[i].__class__.__name__ is "SimpleResponse":
                        if self.hurby.botConfig.bot_name_in_reply:
                            bot_name = self.hurby.botConfig.botname
                            irc.send_message(bot_name + ": " + twitch_cmds[i].respond())
                            # logger.log(logger.INFO, bot_name + ": " + twitch_cmds[i].respond())
                        else:
                            irc.send_message(twitch_cmds[i].respond())
                    else:
                        pass
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
