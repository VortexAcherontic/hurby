from character.character import Character
from character.user_id_types import UserIDType
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import hurby_utils, logger


class GiftCreditsCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data)
        self.answers = json_data["answers"]
        self.error_parse_credits = json_data["error_parse_credits"]
        self.error_recipient = json_data["error_recipient"]
        self.error_insufficient_credits = json_data["error_insufficient_credits"]
        self.error_less_params = json_data["error_less_params"]
        self.hurby = hurby

    def do_command(self, params: list, character: Character):
        irc = self.hurby.twitch_receiver.twitch_listener
        if len(params) < 2:
            msg = hurby_utils.get_random_reply(self.error_less_params)
            irc.send_message(msg)
        elif character is not None:
            char_man = self.hurby.get_char_manager()
            receiving_char_name = params[0].lower()
            receiving_char = char_man.get_character(receiving_char_name, UserIDType.TWITCH)
            if receiving_char is not None:
                try:
                    creds = int(params[1])
                    if character.credits < creds:
                        msg = hurby_utils.get_random_reply(self.error_insufficient_credits)
                        msg = msg.replace("$user_credits", str(character.credits))
                        irc.send_message(msg)
                    else:
                        receiving_char.credits += creds
                        character.credits -= creds
                        receiving_char.save()
                        character.save()
                        msg = hurby_utils.get_random_reply(self.answers)
                        msg = msg.replace("$user", character.twitchid)
                        msg = msg.replace("$recipient", receiving_char.twitchid)
                        msg = msg.replace("$credits", str(creds))
                        irc.send_message(msg)
                except ValueError:
                    msg = hurby_utils.get_random_reply(self.error_parse_credits)
                    irc.send_message(msg)
            else:
                msg = hurby_utils.get_random_reply(self.error_recipient)
                irc.send_message(msg)
        else:
            logger.log(logger.INFO, "Exception: Issuing character is None")
