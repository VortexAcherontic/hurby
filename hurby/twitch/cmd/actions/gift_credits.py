from hurby.character.character import Character
from hurby.character.exceptions.less_than_zero_exception import LessThanZeroException
from hurby.character.user_id_types import UserIDType
from hurby.twitch.cmd.abstract_command import AbstractCommand
from hurby.utils import logger, hurby_utils


class GiftCreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.answers = json_data["answers"]
        self.error_parse_credits = json_data["error_parse_credits"]
        self.error_recipient = json_data["error_recipient"]
        self.error_insufficient_credits = json_data["error_insufficient_credits"]
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
                    creds = int(params[1])
                    if character.get_credits() < creds:
                        msg = hurby_utils.get_random_reply(self.error_insufficient_credits)
                        msg = msg.replace("$user_credits", str(character.get_credits()))
                        self.irc.send_message(msg)
                    else:
                        receiving_char.add_credits(creds)
                        character.remove_credits(creds)
                        receiving_char.save()
                        character.save()
                        msg = hurby_utils.get_random_reply(self.answers)
                        msg = msg.replace("$user", character.twitchid)
                        msg = msg.replace("$recipient", receiving_char.twitchid)
                        msg = msg.replace("$credits", str(creds))
                        self.irc.send_message(msg)
                except LessThanZeroException:
                    msg = hurby_utils.get_random_reply(self.error_parse_credits)
                    self.irc.send_message(msg)
                except ValueError:
                    msg = hurby_utils.get_random_reply(self.error_parse_credits)
                    self.irc.send_message(msg)
            else:
                msg = hurby_utils.get_random_reply(self.error_recipient)
                self.irc.send_message(msg)
        else:
            logger.log(logger.INFO, "Exception: Issuing character is None")
