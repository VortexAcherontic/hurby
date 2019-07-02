from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable
from character.permission_levels import PermissionLevel
from character.user_id_types import UserIDType


class CharacterManager:

    def __init__(self):
        self.chars: list[Character] = None
        self.black_list: Blacklist = Blacklist()
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()

    def get_char(self, user_id, id_type: UserIDType) -> Character:
        if id_type == UserIDType.TWITCH:
            return self._search_char_by_twitch_id(user_id)

    def get_black_list(self) -> Blacklist:
        return self.black_list

    def _search_char_by_twitch_id(self, user_id) -> Character:
        if self.chars is not None:
            for i in range(0, len(self.chars)):
                if self.chars[i].twitchid == user_id:
                    return self.chars[i]
        tmp = Character()
        json_file_name = self._check_reference_table(user_id)
        if json_file_name is not None:
            tmp.load(json_file_name)
        else:
            tmp.init_default_character(user_id)
            tmp.set_twitch_id(user_id)
            self.ref_table.add_to_ref_table(user_id, tmp.uuid)
            tmp.save()
        return tmp

    def _check_reference_table(self, user_id) -> str:
        return self.ref_table.get_json_file_by_user_id(user_id)

    def check_viewer_id(self, user_id_type: UserIDType, user_id):
        if user_id_type == UserIDType.TWITCH:
            if self.chars is not None:
                for i in range(0, len(self.chars)):
                    if self.chars[i].twitchid == user_id:
                        return True
            return self.ref_table.check_user_id(user_id)

    def create_new_character(self, user_id_type: UserIDType, user_id: str, permission_level: PermissionLevel):
        tmp = Character()
        tmp.init_default_character(user_id, permission_level)
        if user_id_type == UserIDType.TWITCH:
            tmp.set_twitch_id(user_id)
        self.ref_table.add_to_ref_table(user_id, tmp.uuid)
        tmp.save()

