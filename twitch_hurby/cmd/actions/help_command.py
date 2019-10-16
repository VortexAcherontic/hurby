import random

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class HelpCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.hurby = hurby
        self.introduction = json_data["introduction"]
        self.cmd_error = json_data["cmd_error"]

    def do_command(self, params: list, character: Character):
        irc = self.hurby.twitch_receiver.twitch_listener
        valid_cmds = ""
        if character is not None:
            if len(params) == 0:
                for x in self.hurby.twitch_receiver.twitch_conf.get_cmds():
                    if x is not None:
                        if character.perm == PermissionLevels.EVERYBODY:
                            if x.permission_level == PermissionLevels.EVERYBODY:
                                valid_cmds += str(x.trigger) + " "
                        elif character.perm == PermissionLevels.MODERATOR:
                            if x.permission_level == PermissionLevels.EVERYBODY or x.permission_level == \
                                    PermissionLevels.MODERATOR:
                                valid_cmds += str(x.trigger) + " "
                        elif character.perm == PermissionLevels.ADMINISTRATOR:
                            valid_cmds += str(x.trigger) + " "
                cur_answer = self.introduction[random.randint(0, len(self.introduction) - 1)]
                cur_answer = cur_answer.replace("$command_list", valid_cmds)
                irc.send_message(cur_answer)
            else:
                response = self.cmd_error[random.randint(0, len(self.cmd_error) - 1)]
                for x in self.hurby.twitch_receiver.twitch_conf.get_cmds():
                    if x is not None:
                        compare = str(params[0])
                        if not compare.startswith("!"):
                            compare = "!" + compare
                        if x.trigger == compare:
                            response = x.description
                irc.send_message(response)
