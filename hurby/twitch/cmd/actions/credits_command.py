import random

from hurby.character.character import Character
from hurby.twitch.cmd.abstract_command import AbstractCommand


class CreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.hurby = hurby
        self.answers = json_data["answers"]

    def do_command(self, params: list, character: Character):
        if character is not None:
            irc = self.hurby.twitch_receiver.twitch_listener
            cur_answer = self.answers[random.randint(0, len(self.answers) - 1)]
            cur_answer = cur_answer.replace("$user_id", character.twitchid)
            cur_answer = cur_answer.replace("$user_credits", str(character.get_credits()))
            irc.send_message(cur_answer)
