from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable
from character.user_id_types import UserIDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import logger


def _is_chars_in_user_ids(user_ids: [str], char: Character, user_id_type: UserIDType):
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


class CharacterManager:

    def __init__(self):
        self.chars: list[Character] = None
        self.black_list: Blacklist = Blacklist()
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()

    def get_character(self, user_id: str, user_id_type: UserIDType, permission_level=PermissionLevels.EVERYBODY,
                      update_perm_level=False):
        tmp_char = self._search_loaded_characters(user_id, user_id_type)
        if tmp_char is None:
            tmp_char = Character()
            if self._is_in_reference_table(user_id):
                json_file = self.ref_table.get_json_file_by_user_id(user_id)
                tmp_char.load(json_file)
                self._add_char_to_table(tmp_char)
            else:
                tmp_char.init_default_character(user_id, permission_level, user_id_type)
                tmp_char.save()
                self._add_char_to_table(tmp_char)
                self._add_char_to_ref_table(tmp_char, user_id_type)
        if update_perm_level:
            logger.log(logger.DEV,
                       "CharacterManager: Updating permission level for " + user_id + " to: " + permission_level.value)
            tmp_char.set_permission_level(permission_level)
            tmp_char.save()
        return tmp_char

    def get_characters(self):
        return self.chars

    def unload_offline_characters(self, user_ids: list, id_type: UserIDType):
        if self.chars is not None:
            for tmp in self.chars:
                if not _is_chars_in_user_ids(user_ids, tmp, id_type):
                    logger.log(logger.DEV, "User offline, unloading: " + str(tmp.twitchid))
                    tmp.save()
                    self.chars.remove(tmp)

    def _add_char_to_table(self, char: Character):
        if self.chars is None:
            self.chars = [char]
        elif self.chars:
            self.chars.append(char)

    def _search_loaded_characters(self, user_id: str, user_id_type: UserIDType):
        if self.chars is not None:
            for tmp in self.chars:
                if tmp is not None:
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

    def _add_char_to_ref_table(self, character: Character, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            self.ref_table.add_to_ref_table(character.twitchid, character.uuid)
