from character.character import Character
from character.user_id_types import UserIDType
from items.base_item import BaseItem
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import hurby_utils, logger


class SpawnItemCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.unknown_item = json_data["unknown_item"]
        self.unknown_user = json_data["unknown_user"]
        self.to_few_args = json_data["to_few_args"]
        self.item_spawned = json_data["item_spawned"]

    def do_command(self, params: list, character: Character):
        if character is not None:
            if len(params) == 2:
                target_str = params[0]
                target: Character = self.hurby.char_manager.get_character(target_str, UserIDType.TWITCH)
                if target is not None:
                    try:
                        int(params[1])
                    except ValueError:
                        msg = hurby_utils.get_random_reply(self.unknown_item)
                        msg = msg.replace("$user", character.twitchid)
                        self.irc.send_message(msg)
                    item_id = int(params[1])
                    item: BaseItem = self.hurby.item_manager.get_item_by_id(item_id)
                    if item is not None:
                        target.inventory.add_item(item)
                        target.save()
                        msg = hurby_utils.get_random_reply(self.item_spawned)
                        msg = msg.replace("$user", character.twitchid)
                        msg = msg.replace("$item", item.name)
                        self.irc.send_message(msg)
                    else:
                        msg = hurby_utils.get_random_reply(self.unknown_item)
                        msg = msg.replace("$user", character.twitchid)
                        self.irc.send_message(msg)
                else:
                    msg = hurby_utils.get_random_reply(self.unknown_user)
                    msg = msg.replace("$user", character.twitchid)
                    self.irc.send_message(msg)
            else:
                msg = hurby_utils.get_random_reply(self.to_few_args)
                msg = msg.replace("$user", character.twitchid)
                self.irc.send_message(msg)
        else:
            logger.log(logger.ERR, "SpawnItemCommand: issuing user is None! This should not have happened :(")
