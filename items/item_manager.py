from items.base_item import BaseItem
from utils import hurby_utils, json_loader, logger
from utils.const import CONST

ITEM_DIR = CONST.DIR_APP_DATA_ABSOLUTE + "/items/"


class ItemManager:
    def __init__(self):
        self.items = [BaseItem]
        self._load_all_items()

    def get_item_by_id(self, id):
        for i in self.items:
            if i.verify_id(id):
                return i
        return None

    def _load_all_items(self):
        all_item_files = hurby_utils.get_all_files_in_path(ITEM_DIR)
        for file in all_item_files:
            if file is not None:
                if file.endswith(".json"):
                    item_json = json_loader.load_json(ITEM_DIR + file)
                    item : BaseItem = BaseItem(item_json)
                    self.items.append(item)
                    logger.log(logger.DEV, "Loaded item: "+item.name)

    def _check_for_duplicate_id(self):
        pass
