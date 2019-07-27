import random

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class CreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = CMDResponseRealms(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm)
        self.hurby = hurby
        self.answers = json_data["answers"]

    def do_command(self, params: list, character: Character):
        irc = self.hurby.twitch_receiver.twitch_listener
        cur_answer = self.answers[random.randint(0, len(self.answers) - 1)]
        cur_answer = cur_answer.replace("$user_id", character.twitchid)
        cur_answer = cur_answer.replace("$user_credits", str(character.credits))
        irc.send_message(cur_answer)
