from builtins import int

from items.base_item import BaseItem


class PlayerInventory:
    def __init__(self, item_dict):
        self._items: dict[BaseItem] = {}
        if item_dict is not None:
            # This check is mandatory because the old framework used list instead of dict
            # If a list is detected it will be automatically overwritten by the empty dict _items
            if item_dict is dict:
                self._items = item_dict
            elif item_dict is list:
                pass

    def add_item(self, item: BaseItem):
        if self._items is list:
            self._items = {}
        free_slot = self._get_free_slot()
        self._items[free_slot] = item

    def remove_item_by_slot(self, slot: int):
        if slot < 0 or slot >= len(self._items):
            # Not a suitable slot
            pass
        if slot == len(self._items) - 1:
            del (self._items[slot])
        else:
            self._items[slot] = None

    def get_item_by_slot(self, slot: int):
        if slot < 0 or slot >= len(self._items):
            return None
        else:
            return self._items[slot]

    def get_all_items(self) -> dict:
        return self._items

    def to_dict(self):
        text = {}
        for i in self._items:
            text[i] = self._items[i].to_dict()
        return text

    def _get_free_slot(self) -> int:
        for i in range(0, len(self._items) - 1):
            if self._items[i] is None:
                return i
        return len(self._items)

    def _init_empty_inventory(self):
        self._items = {}
