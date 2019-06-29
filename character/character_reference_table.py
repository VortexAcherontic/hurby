import json

from utils import json_loader, logger
from utils.const import CONST


class CharacterReferenceTable:
    REF_TABLE_FILE = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + CONST.FILE_CHAR_REF_TABLE

    def __init__(self):
        self.load_ref_table()
        self.map = None

    def load_ref_table(self):
        self.map = json_loader.loadJSON(CharacterReferenceTable.REF_TABLE_FILE)

    def get_json_by_user_id(self, user_id):
        for x in self.map:
            if x == user_id:
                return map[x]
        return None

    def add_to_ref_table(self, uudi: str, user_id: str):
        if self.map is not None:
            if self.map[user_id] is None:
                self.map.update({user_id: uudi})
                self.save_ref_table()
            else:
                return
        else:
            if self.map is None:
                self.map = {}
            self.map[user_id] = uudi + ".json"
            self.save_ref_table()

    def save_ref_table(self):
        logger.log(logger.INFO, self.map)
        with open(CharacterReferenceTable.REF_TABLE_FILE, 'w') as fp:
            json.dump(self.map, fp)
