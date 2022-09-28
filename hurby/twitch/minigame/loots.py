from hurby.character.character import Character
from hurby.character.character_manager import CharacterManager
from hurby.twitch.cmd.enums.permission_levels import PermissionLevels
from hurby.twitch.irc.irc_connector import IRCConnector
from hurby.utils import json_loader, logger, hurby_utils
from hurby.utils.const import CONST


class Loots:
    def __init__(self, char_manager: CharacterManager, twitch_receiver: IRCConnector):
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_LOOTS
        config_data = json_loader.load_json(config_file)
        self.spend_cred_on_loot = config_data["spend_cred_on_loot"]
        self.base_cred_spend = config_data["base_cred_spend"]
        self.mult_by_viewers = config_data["mult_by_viewers"]
        self.thank_you = config_data["thank_you"]
        self.char_manager = char_manager
        self.twitch_receiver = twitch_receiver

    def spend_credits(self, char_issuing: Character):
        if self.spend_cred_on_loot:
            if char_issuing.perm == PermissionLevels.ADMINISTRATOR:
                spend_credits = self.base_cred_spend
                if self.mult_by_viewers:
                    spend_credits *= len(self.char_manager.get_characters())
                for x in self.char_manager.get_characters():
                    x.add_credits(spend_credits)
                logger.log(logger.DEV, "Loots: Spending: " + str(spend_credits) + " credits to all viewers")
                self._send_thank_you(spend_credits)
            else:
                logger.log(logger.DEV, "Loots: " + char_issuing.twitchid + " is not administrator")

    def _send_thank_you(self, spend_credits):
        msg: str = hurby_utils.get_random_reply(self.thank_you)
        msg = msg.replace("$spend_credits", str(spend_credits))
        logger.log(logger.DEV, msg)
        self.twitch_receiver.send_message(msg)
