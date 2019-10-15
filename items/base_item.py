from math import ceil

from items.base_ability import BaseAbility
from items.base_effect import BaseEffect


class BaseItem:
    def __init__(self, item_json):
        self._id = item_json["id"]
        self.name = item_json["name"]
        self.damage = item_json["damage"]
        self.defense = item_json["defense"]
        self.durability_max = item_json["durability_max"]
        self.value = item_json["value"]
        self.use_all_slots = item_json["use_all_slots"]
        self.slots = item_json["slots"]
        self.stats = BaseEffect(item_json["stats"])
        self.ability = BaseAbility(item_json["ability"])
        self.item_broken_feedback = item_json["item_broken_feedback"]
        self.use_feedback = item_json["use_feedback"]
        if "durability" in item_json:
            self._durability = item_json["durability"]

    def is_broken(self):
        return self._durability > 0

    def verify_id(self, identifier):
        return self._id == identifier

    def calc_repair_costs(self):
        return int(ceil(self.value / self.durability_max * self._durability))

    def use(self):
        if self._durability > 0:
            self._durability -= 1
            return True
        return False

    def repair(self):
        self._durability = self.durability_max
