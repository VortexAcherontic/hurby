from abc import abstractmethod

from character.character import Character
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import hurby_utils


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
        if self.cmd_type == CMDType.ACTION:
            self.permission_level = PermissionLevels(cmd_json["perm"])
        elif self.cmd_type == CMDType.MULTI_ACTION:
            self.sub_commands = _load_subcommands(cmd_json["subcommands"])
        self.hurby = hurby
        self.irc = hurby.twitch_receiver.twitch_listener
        if "description" in cmd_json:
            self.description: str = cmd_json["description"]
        else:
            self.description: str = "No description yet"

    def check_permissions(self, char: Character, subcommand=None) -> bool:
        if self.cmd_type == CMDType.ACTION:
            if char is None:
                return self.permission_level == PermissionLevels.EVERYBODY
            hurby_utils.is_permitted(char.perm, self.permission_level)
        elif self.cmd_type == CMDType.MULTI_ACTION:
            return self._permitted_subcommand(subcommand, char)
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

    def _valid_subcommand(self, sub_trigger):
        for sub in self.sub_commands:
            if not self.hurby.botConfig.commands_case_sensitive:
                for trigger in sub["trigger"]:
                    if trigger.lower() == sub_trigger.lower():
                        return True
            else:
                for trigger in sub["trigger"]:
                    if trigger == sub_trigger:
                        return True
        return False

    def _permitted_subcommand(self, sub_trigger, character: Character):
        if self._valid_subcommand(sub_trigger):
            sub_command = self._get_subcommand_by_trigger(sub_trigger)
            if sub_command is not None:
                char_perm = character.perm
                sub_perm = PermissionLevels[sub_command["perm"]]
                return hurby_utils.is_permitted(char_perm, sub_perm)
        return False

    def _get_subcommand_by_trigger(self, sub_trigger):
        for sub in self.sub_commands:
            for trigger in sub["trigger"]:
                if not self.hurby.botConfig.commands_case_sensitive:
                    if trigger.lower() == sub_trigger.lower():
                        return sub
                elif trigger == sub_trigger:
                    return sub
        return None

    @abstractmethod
    def do_command(self, params: list, character: Character):
        pass
