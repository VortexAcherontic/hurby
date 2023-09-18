from character.character import Character
from twitch.cmd.abstract_command import AbstractCommand


class WhisperCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        user_name = character.twitchid
        message = ""
        for s in params:
            message += s + " "
        self.hurby.twitch_receiver.twitch_listener.send_whisper(user_name, message)
