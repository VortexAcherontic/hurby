from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class ShutdownCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        pass
