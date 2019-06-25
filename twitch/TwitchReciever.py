from twitch import TwitchClient

from twitch.TwitchConfig import TwitchConfig
from utils import Logger


class TwitchReceiver:
    def __init__(self, hurby):
        self.hurby = hurby
        twitch_conf = TwitchConfig(self.hurby)
        self.twitch_conf = twitch_conf
        self.client = None
        self.channel = None
        self.connect_twtich()

    def do_command(self, cmd, parameters, character):
        Logger.log(Logger.INFO, "Received cmd: " + cmd)
        twitch_cmds = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                if cmd == twitch_cmds[i].cmd:
                    if twitch_cmds[i].__class__.__name__ is "SimpleResponse":
                        if self.hurby.botConfig.bot_name_in_reply:
                            bot_name = self.hurby.botConfig.botname
                            Logger.log(Logger.INFO, bot_name + ": " + twitch_cmds[i].respond())
                        else:
                            Logger.log(Logger.INFO, twitch_cmds[i].respond())
                    else:
                        pass

    def new_viewer(self, viewer_id):
        pass

    def connect_twtich(self):
        self.client = TwitchClient(client_id=self.twitch_conf.client_id)
        self.channel = self.client.channels.get_by_id(44322889)
        print(self.channel.id)
        print(self.channel.name)
        print(self.channel.display_name)

