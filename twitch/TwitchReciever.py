from utils import Logger


class TwitchReciver:
    def __init__(self, twitch_conf):
        self.twitch_conf = twitch_conf

    def do_command(self, cmd, parameters, character):
        Logger.log(Logger.INFO, "Received cmd: "+cmd)
        twitch_cmds = self.twitch_conf.get_cmds()
        Logger.log(Logger.INFO, "Fetched: "+str(len(twitch_cmds))+" commands from twitch config")
        for i in range(0, len(twitch_cmds)):
            if cmd == twitch_cmds[i].cmd:
                pass