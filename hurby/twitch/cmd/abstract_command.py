from abc import abstractmethod

from hurby.character.character import Character
from hurby.twitch.cmd.enums.cmd_response_realms import CMDResponseRealms
from hurby.twitch.cmd.enums.cmd_types import CMDType
from hurby.twitch.cmd.enums.permission_levels import PermissionLevels
from hurby.utils import hurby_utils


def _load_subcommands(json_data):
    sub_list = []
    for sub in json_data:
        sub_list.append(sub)
    return sub_list


class AbstractCommand:

    def __init__(self, cmd_json: dict, hurby):
        self.trigger = cmd_json["cmd"]
        self.cmd_type: CMDType = CMDType(cmd_json["type"])
        self.realm: CMDResponseRealms = CMDResponseRealms(cmd_json["realm"])
        self.reply = cmd_json["reply"]
        if self.cmd_type == CMDType.ACTION or self.cmd_type == CMDType.REPLY:
            self.permission_level = PermissionLevels(cmd_json["perm"])
        elif self.cmd_type == CMDType.MULTI_ACTION:
            self.sub_commands = _load_subcommands(cmd_json["subcommands"])
        self.hurby = hurby
        self.irc = hurby.twitch_receiver.twitch_listener
        if "description" in cmd_json:
            self.description: str = cmd_json["description"]
        else:
            self.description: str = "No description yet"

    def check_permissions(self, char: Character, parameters=None) -> bool:
        if self.cmd_type == CMDType.ACTION or self.cmd_type == CMDType.REPLY:
            if char is None:
                return self.permission_level == PermissionLevels.EVERYBODY
            return hurby_utils.is_permitted(char.perm, self.permission_level)
        elif self.cmd_type == CMDType.MULTI_ACTION:
            if self._valid_subcommand(parameters):
                return self._permitted_subcommand(parameters, char)
        else:
            return False

    def check_trigger(self, trigger: str) -> bool:
        if isinstance(self.trigger, list):
            for t in self.trigger:
                if self.hurby.botConfig.commands_case_sensitive:
                    if t == trigger:
                        return True
                else:
                    if t.lower() == trigger.lower():
                        return True
        else:
            if self.hurby.botConfig.commands_case_sensitive:
                return self.trigger == trigger
            else:
                return self.trigger.lower() == trigger.lower()

    def _valid_subcommand(self, parameters):
        for sub in self.sub_commands:
            if not self.hurby.botConfig.commands_case_sensitive:
                for trigger in sub["trigger"]:
                    if isinstance(parameters, list):
                        if len(parameters) == 0 and trigger == "":
                            return True
                        else:
                            for param in parameters:
                                if trigger.lower() == param.lower():
                                    return True
                    else:
                        if trigger.lower() == parameters.lower():
                            return True
            else:
                for trigger in sub["trigger"]:
                    if isinstance(parameters, list):
                        for param in parameters:
                            if trigger == param:
                                return True
                    else:
                        if trigger == parameters:
                            return True
        return False

    def _permitted_subcommand(self, parameters, character: Character):
        sub_command = self._get_subcommand_by_trigger(parameters)
        if sub_command is not None:
            char_perm = character.perm
            sub_perm = PermissionLevels(sub_command["perm"])
            return hurby_utils.is_permitted(char_perm, sub_perm)

    def _get_subcommand_by_trigger(self, parameters):
        for sub in self.sub_commands:
            for trigger in sub["trigger"]:
                if isinstance(parameters, list):
                    if len(parameters) == 0:
                        if trigger == "":
                            return sub
                    else:
                        for param in parameters:
                            if not self.hurby.botConfig.commands_case_sensitive:
                                if trigger.lower() == param.lower():
                                    return sub
                            elif trigger == param:
                                return sub
                else:
                    if not self.hurby.botConfig.commands_case_sensitive:
                        if trigger.lower() == parameters.lower():
                            return sub
                    elif trigger == parameters:
                        return sub
        return None

    @abstractmethod
    def do_command(self, params: list, character: Character):
        pass
