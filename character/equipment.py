from items.base_item import BaseItem
from items.item_manager import ItemManager
from utils import logger

SLOTS = {
    "HEAD": "head",
    "NECK": "neck",
    "SHOULDER_LEFT": "shoulder_left",
    "SHOULDER_RIGHT": "shoulder_right",
    "ARM_LEFT": "arm_left",
    "ARM_RIGHT": "arm_right",
    "HAND_LEFT": "hand_left",
    "HAND_RIGHT": "hand_right",
    "TORSO": "torso",
    "HIPS": "hips",
    "LEG_LEFT": "leg_left",
    "LEG_RIGHT": "leg_right",
    "FOOT_LEFT": "foot_left",
    "FOOT_RIGHT": "foot_right"
}


class PlayerEquipment:
    def __init__(self, equip_json: dict, character_uuid: str, item_manager: ItemManager):
        self._equipped = self._init_empty_equip()
        if equip_json is not None:
            self.item_man = item_manager
            for slot in SLOTS:
                if SLOTS[slot] in equip_json:
                    if equip_json[SLOTS[slot]] is not None:
                        # Receiving the items id from the player equip dict to check if the item exists or not
                        tmp_item = self.item_man.dose_item_id_exists(equip_json[SLOTS[slot]].id)
                        if tmp_item is not None:
                            # Creating the item with it's current stats which are only saved in the players inventory.
                            self._equipped[slot] = BaseItem(equip_json[SLOTS[slot]])
                    else:
                        self._equipped[slot] = None
                else:
                    logger.log(logger.WARN, "Slot : " + SLOTS[slot] + " not existing in JSON for: " + character_uuid)

    def get_atk_value_sum(self) -> float:
        summarized = 0
        for i in self._equipped:
            if hasattr(self._equipped[i], "damage"):
                summarized += self._equipped[i].damage
        return summarized

    def get_def_value_sum(self) -> float:
        summarized = 0
        for i in self._equipped:
            if hasattr(self._equipped[i], "defense"):
                summarized += self._equipped[i].defense
        return summarized

    def unequip_item(self, identifier: int) -> bool:
        if self._has_item(identifier):
            item: BaseItem = self.item_man.get_item_by_id(identifier)
            if item.use_all_slots:
                for s in item.slots:
                    if s in self._equipped:
                        self._equipped[s] = None
                    else:
                        logger.log(logger.ERR, "Can't unequip item: " + item.name + " invalid slot: " + s)
                        return False
                return True
            else:
                for s in item.slots:
                    if s in self._equipped:
                        i: BaseItem = self._equipped[s]
                        if i is not None:
                            if i.verify_id(identifier):
                                self._equipped[s] = None
                                return True
                    else:
                        logger.log(logger.ERR, "Can't unequip item: " + item.name + " invalid slot: " + s)
                        return False
        return False

    def equip_item(self, identifier: int) -> bool:
        item = self.item_man.get_item_by_id(identifier)
        if self._has_free_slot(item):
            if item.use_all_slots:
                for s in item.slots:
                    self._equipped[s] = item
            else:
                for s in item.slots:
                    if self._equipped[s] is not None:
                        self._equipped[s] = item
            return True
        return False

    def use_item(self, identifier: int) -> bool:
        if self._has_item(identifier):
            for s in self._equipped:
                i: BaseItem = self._equipped[s]
                if i is not None:
                    if i.verify_id(identifier):
                        i.use()
                        return True
        return False

    def to_dict(self):
        return self._equipped

    def _has_free_slot(self, item: BaseItem) -> bool:
        use_all = item.use_all_slots
        slots = item.slots
        if use_all:
            for s in slots:
                if s in self._equipped:
                    if self._equipped[slots[s]] is not None:
                        return False
                else:
                    logger.log(logger.ERR, "Can not equip " + item.name + " because of slot mismatch: " + s)
                    return False
            return True
        else:
            for s in slots:
                if self._equipped[slots[s]] is None:
                    return True

    def _has_item(self, identifier: int) -> bool:
        for s in self._equipped:
            if self._equipped[s] is not None:
                item: BaseItem = self._equipped[s]
                if item.verify_id(identifier):
                    return True
        return False

    @staticmethod
    def _init_empty_equip() -> dict:
        empty_equip = {}
        for s in SLOTS:
            empty_equip[SLOTS[s]] = None
        return empty_equip
