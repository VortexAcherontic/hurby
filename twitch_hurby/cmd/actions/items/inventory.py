from orca import logger

from character.character import Character
from character.inventory import PlayerInventory
from character.user_id_types import UserIDType
from items.base_item import BaseItem
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import hurby_utils, logger


class InventoryCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.reply_inv = json_data["reply_inv"]
        self.reply_empty_inv = json_data["reply_empty_inv"]

    def do_command(self, params: list, character: Character):
        if character is not None:
            inv: dict[BaseItem] = character.inventory.get_all_items()
            if inv is not None and len(inv) > 0:
                msg = hurby_utils.get_random_reply(self.reply_inv)
                msg = msg.replace("$user", character.twitchid)
                for i in inv:
                    dur = str(inv[i].get_durability())
                    dur_max = str(inv[i].durability_max)
                    item_msg = " "+i+": "+inv[i].name+" ("+dur+"/"+dur_max+") |"
                    msg += item_msg
                self.irc.send_message(msg)
            else:
                msg = hurby_utils.get_random_reply(self.reply_empty_inv)
                msg = msg.replace("$user", character.twitchid)
                self.irc.send_message(msg)
        else:
            logger.log(logger.WARN, "A none character tried to issue a command!")
