import random

from character.character import Character
from character.user_id_types import UserIDType
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import logger


class AddCreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = CMDResponseRealms(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        description = json_data["description"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm, description)
        self.error_less_params = json_data["error_less_params"]
        self.hurby = hurby

    def do_command(self, params: list, character: Character):
        irc = self.hurby.twitch_receiver.twitch_listener
        if len(params) < 2:
            msg = self.error_less_params[random.randint(0, len(self.error_less_params) - 1)]
            irc.send_message(msg)
        elif character is not None:
            char_man = self.hurby.get_char_manager()
            receiving_char_name = params[0].lower()
            receiving_char = char_man.get_character(receiving_char_name, UserIDType.TWITCH)
            if receiving_char is not None:
                try:
                    set_cred = int(params[1])
                    receiving_char.credits = set_cred
                    receiving_char.save()
                    logger.log(logger.INFO, receiving_char.twitchid + " has now " + str(set_cred) + "Credits")
                except ValueError:
                    logger.log(logger.INFO, "Exception: Unable to set credits")
            else:
                logger.log(logger.INFO, "Exception: Receiving character is None: " + receiving_char_name)
        else:
            logger.log(logger.INFO, "Exception: Issuing character is None")
