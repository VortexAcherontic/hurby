import json

from character.blacklist import Blacklist
from character.character import Character
from character.character_reference_table import CharacterReferenceTable
from utils import logger, json_loader
from utils.const import CONST


class CharacterManager:
    ID_TYPE_TWITCH = "twitch"
    ID_TYPE_YOUTUBE = "yt"

    def __init__(self):
        self.chars = [None]
        self.black_list = Blacklist()
        self.ref_table = CharacterReferenceTable()

    # This will check if a user with an id, wether it is twitch_hurby, YouTube or what ever, already is loaded
    # Retruns true a matching character is oaded and false if not
    def get_char(self, user_id, id_type) -> Character:
        if id_type == CharacterManager.ID_TYPE_TWITCH:
            return self.search_char_by_twitch_id(user_id)

    # THis will load a matching JSON by it's id. Character jsons are just counted starting by 0
    # 0.json would be the first ever created character
    # 1.json would be the 2nd char and so on
    # And will load it to the self.chars array
    def load_char(self, json_id):
        pass

    # This will store a character on disk if a user will leave the stream or disconnect from discord
    def save_char(self, char: Character):
        data = self.char_to_json(char)
        file = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + str(char.uuid) + ".json"
        json_loader.save_json(file, data)
        # with open(file, 'w', encoding='utf-8') as outfile:
        # json.dump(data, outfile, ensure_ascii=False, indent=2)

    # This will create a new default character based on the users id and the id type.
    # The ID type is basically determined by the platfrom the user has appeard
    def new_char(self, user_id, user_id_type) -> Character:
        char = Character()
        char.init_default_character(user_id)
        if user_id_type == CharacterManager.ID_TYPE_TWITCH:
            char.twitchid = user_id
        self.save_char(char)
        return char

    def char_to_json(self, char: Character):
        text = [{
            "uuid": char.uuid,
            "name": char.name,
            "credits": char.credits,
            "endurance_cur": char.endurance,
            "endurance_max": char.endurance_max,
            "discordid": char.discordid,
            "twitchid": char.twitchid,
            "youtubeid": char.youtubeid,
            "twitterid": char.twitterid,
            "mail": [char.mails],
            "inventroy": [char.inventory]
        }]
        return text

    def get_black_list(self):
        return self.black_list

    def search_char_by_twitch_id(self, id):
        if self.chars is not None:
            for i in range(0, len(self.chars)):
                cur = self.chars[i]
                if cur is not None and cur.twitchid == id:
                    return cur
        tmp = self.new_char(user_id=id, user_id_type=CharacterManager.ID_TYPE_TWITCH)
        self.chars.append(tmp)
        self.ref_table.add_to_ref_table(str(tmp.uuid), tmp.twitchid)
        return tmp
