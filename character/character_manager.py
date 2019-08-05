from typing import List

from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable
from character.permission_levels import PermissionLevel
from character.user_id_types import UserIDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import logger


class CharacterManager:

    def __init__(self):
        self.chars: list[Character] = None
        self.black_list: Blacklist = Blacklist()
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()

    def get_character(self, user_id: str, user_id_type: UserIDType, permission_level=PermissionLevels.EVERYBODY):
        tmp_char = self._search_loaded_characters(user_id, user_id_type)
        if tmp_char is None:
            tmp_char = Character()
            if self._is_in_reference_table(user_id):
                json_file = self.ref_table.get_json_file_by_user_id(user_id)
                tmp_char.load(json_file)
                return tmp_char
            else:
                tmp_char.init_default_character(user_id, permission_level, user_id_type)
        else:
            return tmp_char

    def unload_offline_characters(self, user_ids: list, id_type: UserIDType):
        if self.chars is not None:
            for i in range(0, len(self.chars)):
                cur_char = self.chars[i]
                if not self._is_chars_in_user_ids(user_ids, cur_char, id_type):
                    logger.log(logger.INFO, "User offline, unloading: " + cur_char.twitchid)
                    cur_char.save()
                    self.chars.remove(cur_char)

    def _is_chars_in_user_ids(self, user_ids: [str], char: Character, user_id_type: UserIDType):
        for x in user_ids:
            if user_id_type == UserIDType.TWITCH:
                if char.twitchid == x:
                    return True
            elif user_id_type == UserIDType.TWITTER:
                pass
            elif user_id_type == UserIDType.PATREON:
                pass
            elif user_id_type == UserIDType.YOUTUBE:
                pass
            elif user_id_type == UserIDType.STEAM:
                pass
            elif user_id_type == UserIDType.TELEGRAM:
                pass
            elif user_id_type == UserIDType.DISCORD:
                pass
            else:
                return False
        return False

    def _search_loaded_characters(self, user_id: str, user_id_type: UserIDType):
        if self.chars is not None:
            for tmp in self.chars:
                if user_id_type == UserIDType.TWITCH:
                    if user_id == tmp.twitchid:
                        return tmp
                elif user_id_type == UserIDType.TWITTER:
                    pass
                elif user_id_type == UserIDType.PATREON:
                    pass
                elif user_id_type == UserIDType.YOUTUBE:
                    pass
                elif user_id_type == UserIDType.STEAM:
                    pass
                elif user_id_type == UserIDType.DISCORD:
                    pass
        return None

    def _is_in_reference_table(self, user_id: str):
        return self.ref_table.check_user_id(user_id)
