from character.character import Character
from character.character_manager import CharacterManager
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from twitch_hurby.irc.irc_connector import IRCConnector
from utils import json_loader, logger, hurby_utils
from utils.const import CONST


class Loots:
    def __init__(self, char_manager: CharacterManager, irc_connector: IRCConnector):
        config_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_LOOTS
        config_data = json_loader.load_json(config_file)
        self.spend_cred_on_loot = config_data["spend_cred_on_loot"]
        self.base_cred_spend = config_data["base_cred_spend"]
        self.mult_by_viewers = config_data["mult_by_viewers"]
        self.thank_you = config_data["thank_you"]
        self.char_manager = char_manager
        self.irc = irc_connector

    def spend_credits(self, char_issuing: Character):
        if self.spend_cred_on_loot:
            if char_issuing.perm == PermissionLevels.ADMINISTRATOR:
                spend_credits = self.base_cred_spend
                if self.mult_by_viewers:
                    spend_credits *= len(self.char_manager.get_character())
                for x in self.char_manager.get_characters():
                    x.add_credits(spend_credits)
                logger.log(logger.DEV, "Loots: Spending: " + str(spend_credits) + "to all viewers")

    def _send_thank_you(self, spend_credits):
        msg: str = hurby_utils.get_random_reply(self.thank_you)
        msg.replace("$spend_credits", str(spend_credits))
        self.irc.send_message(msg)
