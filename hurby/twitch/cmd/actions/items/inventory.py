from hurby.character.character import Character
from hurby.items.base_item import BaseItem
from hurby.twitch.cmd.abstract_command import AbstractCommand
from hurby.utils import logger, hurby_utils


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
