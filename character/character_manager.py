from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable


class CharacterManager:
    ID_TYPE_TWITCH = "twitch"
    ID_TYPE_YOUTUBE = "yt"
    ID_TYPE_TWITTER = "twitter"
    ID_TYPE_PATREON = "patreon"

    def __init__(self):
        self.chars: list[Character] = None
        self.black_list: Blacklist = Blacklist()
        self.ref_table: CharacterReferenceTable = CharacterReferenceTable()

    def get_char(self, user_id, id_type) -> Character:
        if id_type == CharacterManager.ID_TYPE_TWITCH:
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
