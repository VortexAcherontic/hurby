from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand


class WhisperCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        pass
