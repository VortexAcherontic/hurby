from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.irc.irc_cmd import IRCCommand
from twitch_hurby.irc.irc_connector import IRCConnector
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger


class TwitchReceiver:
    def __init__(self, hurby):
        self.hurby = hurby
        self.twitch_conf = TwitchConfig(self.hurby)
        self.helix = None
        self.twitch_listener = None
        self.connect_twitch_irc()

    def do_command(self, cmd: IRCCommand, char: Character, irc: IRCConnector):
        logger.log(logger.INFO, "Received cmd:\"" + cmd.cmd + "\"")
        logger.log(logger.INFO, "Params:")
        logger.log(logger.INFO, cmd.params)
        twitch_cmds: list[AbstractCommand] = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                tmp: AbstractCommand = twitch_cmds[i]
                if tmp.check_trigger(cmd.cmd):
                    if tmp.check_permissions(char):
                        tmp.do_command(cmd.params, character=char)
                        return
                    elif char is not None:
                        logger.log(logger.INFO, char.twitchid + " has no permission to execute: " + cmd.cmd)
                        return
        self.hurby.twitch_receiver.twitch_listener.send_message(self.hurby.botConfig.get_unknown_cmd_response())

    def connect_twitch_irc(self):
        self.twitch_listener = IRCConnector(self.twitch_conf.bot_username, self.twitch_conf.oauth_token, self, 1,
                                            self.twitch_conf, self.hurby)

    def get_twitch_irc_connector(self) -> IRCConnector:
        return self.twitch_listener
