from character.character import Character
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class AbstractCommand:

    def __init__(self, trigger: str, cmd_type: CMDType, realm: CMDResponseRealms, reply: list,
                 perm: PermissionLevels):
        self.trigger = trigger
        self.cmd_type: CMDType = cmd_type
        self.realm: CMDResponseRealms = realm
        self.reply = reply
        self.permission_level = perm

    def check_permissions(self, char: Character) -> bool:
        pass

    def check_trigger(self, trigger: str) -> bool:
        return self.trigger == trigger

    def do_command(self, params: list):
        pass
