from typing import List

from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable
from character.permission_levels import PermissionLevel
from character.user_id_types import UserIDType
from utils import logger


class CharacterManager:

    def __init__(self):
        self.chars: list[Character] = None
        self.black_list: Blacklist = Blacklist()
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()

    def get_char(self, user_id, id_type: UserIDType) -> Character:
        if id_type == UserIDType.TWITCH:
            return self._search_char_by_twitch_id(user_id)

    def load_character(self, user_id: str, id_type: UserIDType):
        if not self._is_character_loaded(user_id=user_id, id_type=id_type):
            self._load_character(user_id=user_id, id_type=id_type)

    def get_black_list(self) -> Blacklist:
        return self.black_list

    def check_viewer_id(self, user_id_type: UserIDType, user_id):
        if user_id_type == UserIDType.TWITCH:
            if self.chars is not None:
                for i in range(0, len(self.chars)):
                    if self.chars[i].twitchid == user_id:
                        return True
            return self.ref_table.check_user_id(user_id)

    def create_new_character(self, user_id_type: UserIDType, user_id: str, permission_level: PermissionLevel):
        tmp = Character()
        tmp.init_default_character(user_id,  permission_level=permission_level, user_id_type=user_id_type)
        if user_id_type == UserIDType.TWITCH:
            tmp.set_twitch_id(user_id)
        self.ref_table.add_to_ref_table(user_id, tmp.uuid)
        if self.chars is None:
            self.chars = [tmp]
        else:
            self.chars.append(tmp)
        tmp.save()

    def unload_offline_character(self, user_ids: List[str], user_id_type: UserIDType):
        logger.log(logger.INFO, "Check for offline chatters:")
        logger.log(logger.INFO, user_ids)
        if self.chars is not None:
            for c in self.chars:
                char_in_uids = False
                for uid in user_ids:
                    if user_id_type == UserIDType.TWITCH:
                        if c.twitchid == uid:
                            char_in_uids = True
                if not char_in_uids:
                    logger.log(logger.INFO, "Character: " + c.twitchid + " is offline, unloading ....")
                    c.save()
                    self.chars.remove(c)

    def _search_char_by_twitch_id(self, user_id) -> Character:
        if self.chars is not None:
            for i in range(0, len(self.chars)):
                if self.chars[i].twitchid == user_id:
                    return self.chars[i]
        return None

    def _check_reference_table(self, user_id) -> str:
        return self.ref_table.get_json_file_by_user_id(user_id)

    def _load_character(self, user_id: str, id_type: UserIDType):
        if not self._is_character_loaded(user_id, id_type):
            user_json_file = self.ref_table.get_json_file_by_user_id(user_id)
            tmp = Character()
            tmp.load(user_json_file)
            if self.chars is None:
                self.chars = [tmp]
            else:
                self.chars.append(tmp)

    def _is_character_loaded(self, user_id: str, id_type: UserIDType):
        if self.chars is not None:
            for i in range(0, len(self.chars)):
                if id_type == UserIDType.TWITCH:
                    if self.chars[i].twitchid == user_id:
                        logger.log(logger.INFO, "Character: " + user_id + " is already loaded")
                        return True
        return False
