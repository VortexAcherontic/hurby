import random

from hurby.character.character import Character
from hurby.twitch.cmd.abstract_command import AbstractCommand


class SimpleResponse(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        if self.hurby.botConfig.bot_name_in_reply:
            bot_name = self.hurby.botConfig.botname
            self.irc.send_message(bot_name + ": " + self._random_response())
        else:
            self.irc.send_message(self._random_response())

    def _random_response(self):
        if isinstance(self.reply, list):
            return self.reply[random.randint(0, len(self.reply) - 1)]
        else:
            return self.reply
