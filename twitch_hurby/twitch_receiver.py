import pydle
from twitch import TwitchHelix
from character.character import Character
from twitch_hurby.twitch_config import TwitchConfig
from twitch_hurby.twitch_irc_bot import TwitchIRCBot
from utils import logger


class TwitchReceiver:
    def __init__(self, hurby):
        self.hurby = hurby
        twitch_conf = TwitchConfig(self.hurby)
        self.twitch_conf = twitch_conf
        self.helix = None
        self.twitch_listener = None
        self.connect_twitch_irc()
        self.connect_twitch_helix()

    def do_command(self, cmd, parameters, character: Character):
        logger.log(logger.INFO, "Received cmd: " + cmd)
        twitch_cmds = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                if cmd == twitch_cmds[i].cmd:
                    if twitch_cmds[i].__class__.__name__ is "SimpleResponse":
                        if self.hurby.botConfig.bot_name_in_reply:
                            bot_name = self.hurby.botConfig.botname
                            logger.log(logger.INFO, bot_name + ": " + twitch_cmds[i].respond())
                        else:
                            logger.log(logger.INFO, twitch_cmds[i].respond())
                    else:
                        pass

    def connect_twitch_helix(self):
        self.helix = TwitchHelix(client_id=self.twitch_conf.client_id, oauth_token=self.twitch_conf.oauth_token)

    def connect_twitch_irc(self):
        self.twitch_listener = TwitchIRCBot("zrayentertainment", self.twitch_conf.oauth_token).start()

    def get_irc_listener(self) -> TwitchIRCBot:
        return self.twitch_listener
