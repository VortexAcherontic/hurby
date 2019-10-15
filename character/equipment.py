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
    def __init__(self, equip_json, character_id, item_manager: ItemManager):
        self.item_man = item_manager
        self.equipped = self._init_empty_equip()
        for slot in SLOTS:
            if SLOTS[slot] in equip_json:
                self.equipped[slot] = self.item_man.get_item_by_id(equip_json[SLOTS[slot]])
            else:
                logger.log(logger.WARN, "Slot : " + SLOTS["slot"] + " not existing in JSON for: " + character_id)

    def get_atk_value_sum(self):
        summarized = 0
        for i in self.equipped:
            if hasattr(self.equipped[i], "damage"):
                summarized += self.equipped[i].damage
        return summarized

    def get_def_value_sum(self):
        summarized = 0
        for i in self.equipped:
            if hasattr(self.equipped[i], "defense"):
                summarized += self.equipped[i].defense
        return summarized

    def unequip_item(self, identifier: int):
        if self._has_item(identifier):
            item: BaseItem = self.item_man.get_item_by_id(identifier)
            if item.use_all_slots:
                for s in item.slots:
                    if s in self.equipped:
                        self.equipped[s] = None
                    else:
                        logger.log(logger.ERR, "Can't unequip item: " + item.name + " invalid slot: " + s)
                        return False
                return True
            else:
                for s in item.slots:
                    if s in self.equipped:
                        i: BaseItem = self.equipped[s]
                        if i is not None:
                            if i.verify_id(identifier):
                                self.equipped[s] = None
                                return True
                    else:
                        logger.log(logger.ERR, "Can't unequip item: " + item.name + " invalid slot: " + s)
                        return False
        return False

    def equip_item(self, identifier: int):
        item = self.item_man.get_item_by_id(identifier)
        if self._has_free_slot(item):
            if item.use_all_slots:
                for s in item.slots:
                    self.equipped[s] = item
            else:
                for s in item.slots:
                    if self.equipped[s] is not None:
                        self.equipped[s] = item
            return True
        return False

    def use_item(self, identifier: int):
        if self._has_item(identifier):
            for s in self.equipped:
                i: BaseItem = self.equipped[s]
                if i is not None:
                    if i.verify_id(identifier):
                        i.use()
                        return True
        return False

    def _has_free_slot(self, item: BaseItem):
        use_all = item.use_all_slots
        slots = item.slots
        if use_all:
            for s in slots:
                if s in self.equipped:
                    if self.equipped[slots[s]] is not None:
                        return False
                else:
                    logger.log(logger.ERR, "Can not equip " + item.name + " because of slot mismatch: " + s)
                    return False
            return True
        else:
            for s in slots:
                if self.equipped[slots[s]] is None:
                    return True

    def _has_item(self, identifier: int):
        for s in self.equipped:
            if self.equipped[s] is not None:
                item: BaseItem = self.equipped[s]
                if item.verify_id(identifier):
                    return True
        return False

    @staticmethod
    def _init_empty_equip():
        empty_equip = {}
        for s in SLOTS:
            empty_equip[s] = None
        return empty_equip
