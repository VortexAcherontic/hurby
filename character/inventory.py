from builtins import int

from items import base_item
from items.base_item import BaseItem


class PlayerInventory:
    def __init__(self, inv_dict, hurby):
        self._items: dict[BaseItem] = {}
        self.hurby = hurby
        if inv_dict is not None and isinstance(inv_dict, dict):
            self._convert_inv_ref_dict_to_item(inv_dict)

    def add_item(self, item: BaseItem):
        if self._items is list:
            self._items = {}
        free_slot = self._get_free_slot()
        self._items[free_slot] = item

    def remove_item_by_slot(self, slot: int) -> bool:
        if slot < 0 or slot >= len(self._items):
            return False
        if slot == len(self._items) - 1:
            del (self._items[slot])
            return True
        else:
            self._items[slot] = None
            return True

    def get_item_by_slot(self, slot: int) -> BaseItem:
        if slot < 0 or slot >= len(self._items):
            return None
        else:
            return self._items[slot]

    def get_all_items(self) -> dict:
        return self._items

    def to_dict(self) -> dict:
        text = {}
        for i in self._items:
            text[i] = self._items[i].to_dict_only_reference()
        return text

    def _get_free_slot(self) -> int:
        for i in range(0, len(self._items) - 1):
            if self._items[i] is None:
                return i
        return len(self._items)

    def _convert_inv_ref_dict_to_item(self, inv_reference_dict: dict):
        for i in inv_reference_dict:
            item_id = inv_reference_dict[i][base_item.KEY_ID]
            durability = inv_reference_dict[i][base_item.KEY_DURABILITY]
            tmpItem: BaseItem = self.hurby.item_manager.get_item_by_id(item_id)
            tmpItem.set_changeable_params(base_item.KEY_DURABILITY, durability)
            self._items[i] = tmpItem
