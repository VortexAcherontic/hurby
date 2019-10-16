from items.base_item import BaseItem
from utils import hurby_utils, json_loader, logger
from utils.const import CONST

ITEM_DIR = CONST.DIR_APP_DATA_ABSOLUTE + "/items/"


class ItemManager:
    def __init__(self):
        self.items = [BaseItem] * 0
        self._load_all_items()

    def get_item_by_id(self, identifier: int) -> BaseItem:
        for i in self.items:
            if i.verify_id(identifier):
                return i
        return None

    def dose_item_id_exists(self, identifier) -> bool:
        for i in self.items:
            if i.verify_id(identifier):
                return True
        return False

    def _load_all_items(self):
        all_item_files = hurby_utils.get_all_files_in_path(ITEM_DIR)
        for file in all_item_files:
            if file is not None:
                if file.endswith(".json"):
                    item_json = json_loader.load_json(ITEM_DIR + file)
                    item: BaseItem = BaseItem(item_json)
                    if not self._check_for_duplicate_id(item.get_id()):
                        self.items.append(item)
                        logger.log(logger.DEV, "Loaded item: " + item.name)
                    else:
                        logger.log(logger.WARN, "Found conflicting ids, item "+item.name+" was not loaded")

    def _check_for_duplicate_id(self, identifier: int) -> bool:
        for i in self.items:
            if i.verify_id(identifier):
                return True
        return False
