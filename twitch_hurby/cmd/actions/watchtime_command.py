import random

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand


class WatchtimeCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.hurby = hurby
        self.answers = json_data["answers"]

    def do_command(self, params: list, character: Character):
        if character is not None:
            irc = self.hurby.twitch_receiver.twitch_listener
            cur_answer = self.answers[random.randint(0, len(self.answers) - 1)]
            cur_answer = cur_answer.replace("$user_id", character.twitchid)
            cur_answer = cur_answer.replace("$watchtime", str(character.watchtime_min))
            irc.send_message(cur_answer)

    def _prettyfi_time(self, minutes):
        time = minutes
        if minutes > 60 :
            time = time % 60
        return time
