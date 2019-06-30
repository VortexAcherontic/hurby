import random

from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums import cmd_response_realms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class SimpleResponse(AbstractCommand):
    def __init__(self, json_data, hurby):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = cmd_response_realms.get_realm(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm)
        self.hurby = hurby

    def get_cmd(self):
        return self.cmd

    def do_command(self, params: list):
        irc = self.hurby.twitch_receiver.twitch_listener
        if self.hurby.botConfig.bot_name_in_reply:
            bot_name = self.hurby.botConfig.botname
            irc.send_message(bot_name + ": " + self._random_response())
        else:
            irc.send_message(self._random_response())

    def _random_response(self):
        if isinstance(self.reply, list):
            return self.reply[random.randint(0, len(self.reply) - 1)]
        else:
            return self.reply
