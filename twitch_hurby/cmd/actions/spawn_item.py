from character.character import Character
from character.user_id_types import UserIDType
from twitch_hurby.cmd.abstract_command import AbstractCommand


class SpawnItemCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.hurby = hurby

    def do_command(self, params: list, character: Character):
        if len(params) == 2:
            if character is not None:
                target_str = params[0]
                target : Character = self.hurby.char_manager.get_character(target_str, UserIDType.TWITCH)
                if target is not None:
                    if params[1] is int and params[1] >= 0:
                        item_id = params[1]
                        item = self.hurby.item_manager.get_item_by_id(item_id)
                        if item is not None:
                            target.inventory.add_item(item)

