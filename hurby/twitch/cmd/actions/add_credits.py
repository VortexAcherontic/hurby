from character.character import Character
from character.user_id_types import UserIDType
from twitch.cmd.abstract_command import AbstractCommand
from utils import logger, hurby_utils


class AddCreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.error_less_params = json_data["error_less_params"]

    def do_command(self, params: list, character: Character):
        if len(params) < 2:
            msg = hurby_utils.get_random_reply(self.error_less_params)
            self.irc.send_message(msg)
        elif character is not None:
            char_man = self.hurby.char_manager
            receiving_char_name = params[0].lower()
            receiving_char = char_man.get_character(receiving_char_name, UserIDType.TWITCH)
            if receiving_char is not None:
                try:
                    add_cred = int(params[1])
                    mem = receiving_char.get_credits()
                    if add_cred < 0:
                        receiving_char.remove_credits(add_cred*-1)
                    else:
                        receiving_char.add_credits(add_cred)
                    logger.log(logger.INFO, receiving_char.twitchid + " had " + str(mem) + " credits and now " + str(
                        receiving_char.get_credits()))
                except ValueError:
                    logger.log(logger.WARN,
                               "Exception: Unable to set credits please enter a number instead of: " + params[1])
            else:
                logger.log(logger.WARN, "Exception: Receiving character is None: " + receiving_char_name)
        else:
            logger.log(logger.WARN, "Exception: Issuing character is None")
