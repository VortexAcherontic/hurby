import json

from utils import json_loader, logger
from utils.const import CONST


class CharacterReferenceTable:
    REF_TABLE_FILE = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + CONST.FILE_CHAR_REF_TABLE

    def __init__(self):
        self.map = None
        self._load_table()

    def get_json_file_by_user_id(self, user_id):
        if self.map is not None:
            for x in self.map:
                if x == user_id:
                    logger.log(logger.INFO, "User known: " + user_id)
                    return self.map[x]
        else:
            return None

    def add_to_ref_table(self, user_id: str, uudi: str):
        if self.map is None:
            self.map = {}
        self.map[user_id] = uudi + ".json"
        self.save()

    def save(self):
        logger.log(logger.INFO, self.map)
        with open(CharacterReferenceTable.REF_TABLE_FILE, 'w') as fp:
            json.dump(self.map, fp)

    def check_user_id(self, user_id):
        if self.map is not None:
            try:
                return self.map[user_id] is not None
            except KeyError as e:
                return False
        return False

    def _load_table(self):
        self.map = json_loader.loadJSON(CharacterReferenceTable.REF_TABLE_FILE)
