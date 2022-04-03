from hurby.character.character import Character
from hurby.twitch.cmd.abstract_command import AbstractCommand


class ShutdownCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        pass
