from math import ceil

from items.base_ability import BaseAbility
from items.base_stats import BaseStats

KEY_ID = "id"
KEY_DURABILITY = "durability"

class BaseItem:
    def __init__(self, item_json: dict):
        self._id = item_json["id"]
        self.name = item_json["name"]
        self.damage = item_json["damage"]
        self.defense = item_json["defense"]
        self.durability_max = item_json["durability_max"]
        self.value = item_json["value"]
        self.use_all_slots = item_json["use_all_slots"]
        self.slots = item_json["slots"]
        self.stats = BaseStats(item_json["stats"])
        self.ability = BaseAbility(item_json["ability"])
        self.item_broken_feedback = item_json["item_broken_feedback"]
        self.use_feedback = item_json["use_feedback"]
        if "durability" in item_json:
            self._durability = item_json["durability"]
        else:
            self._durability = self.durability_max

    def set_changeable_params(self, param, value):
        if param == "durability":
            self._durability = value

    def get_id(self) -> int:
        return self._id

    def get_durability(self) -> int:
        return self._durability

    def is_broken(self):
        return self._durability > 0

    def verify_id(self, identifier: int) -> bool:
        return self._id == identifier

    def calc_repair_costs(self):
        return int(ceil(self.value / self.durability_max * self._durability))

    def use(self) -> bool:
        if self._durability > 0:
            self._durability -= 1
            return True
        return False

    def repair(self):
        self._durability = self.durability_max

    def to_dict(self) -> dict:
        this = {
            "id": self._id,
            "name": self.name,
            "damage": self.damage,
            "defense": self.defense,
            "durability_max": self.durability_max,
            "value": self.value,
            "use_all_slots": self.use_all_slots,
            "slots": self.slots,
            "stats": self.stats.to_dict(),
            "ability": self.ability.to_dict(),
            "item_broken_feedback": self.item_broken_feedback,
            "use_feedback": self.use_feedback,
            "durability": self._durability
        }
        return this

    def to_dict_only_reference(self):
        this = {
            "id": self._id,
            "durability": self._durability
        }
        return this
