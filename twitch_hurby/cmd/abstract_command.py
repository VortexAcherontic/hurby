from character.character import Character
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class AbstractCommand:

    def __init__(self, trigger: str, cmd_type: CMDType, realm: CMDResponseRealms, reply: list,
                 perm: PermissionLevels, description="No description yet"):
        self.trigger = trigger
        self.cmd_type: CMDType = cmd_type
        self.realm: CMDResponseRealms = realm
        self.reply = reply
        self.permission_level = perm
        self.description: str = description

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
        return self.trigger == trigger

    def do_command(self, params: list, character: Character):
        pass
