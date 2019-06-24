from twitch.cmd import SimpleResponse
from utils import Logger


class TwitchReceiver:
    def __init__(self, twitch_conf):
        self.twitch_conf = twitch_conf

    def do_command(self, cmd, parameters, character):
        Logger.log(Logger.INFO, "Received cmd: "+cmd)
        twitch_cmds = self.twitch_conf.get_cmds()
        for i in range(0, len(twitch_cmds)):
            if twitch_cmds[i] is not None:
                if cmd == twitch_cmds[i].cmd:
                    if twitch_cmds[i].__class__.__name__ is "SimpleResponse":
                        Logger.log(Logger.INFO, twitch_cmds[i].respond())
                    else:
                        pass