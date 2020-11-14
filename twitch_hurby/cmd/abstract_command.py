from abc import abstractmethod

from character.character import Character
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class AbstractCommand:

    def __init__(self, cmd_json: dict, hurby):
        self.trigger = cmd_json["cmd"]
        self.cmd_type: CMDType = CMDType(cmd_json["type"])
        self.realm: CMDResponseRealms = CMDResponseRealms(cmd_json["realm"])
        self.reply = cmd_json["reply"]
        self.permission_level = PermissionLevels(cmd_json["perm"])
        self.hurby = hurby
        self.irc = hurby.twitch_receiver.twitch_listener
        if "description" in cmd_json:
            self.description: str = cmd_json["description"]
        else:
            self.description: str = "No description yet"

    def check_permissions(self, char: Character) -> bool:
        if char is None:
            return self.permission_level == PermissionLevels.EVERYBODY
        if self.permission_level == PermissionLevels.EVERYBODY:
            return True
        if self.permission_level == PermissionLevels.MODERATOR:
            return char.perm == PermissionLevels.MODERATOR or char.perm == PermissionLevels.ADMINISTRATOR
        if self.permission_level == PermissionLevels.ADMINISTRATOR:
            return char.perm == PermissionLevels.ADMINISTRATOR

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

    @abstractmethod
    def do_command(self, params: list, character: Character):
        pass
