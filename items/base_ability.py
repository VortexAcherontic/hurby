ABILITY_TYPES = {
    "BLIND": "blind"
}


class BaseAbility:
    def __init__(self, ability_json):
        self._abilities = {}
        for a in ABILITY_TYPES:
            if ABILITY_TYPES[a] in ability_json:
                self._abilities[a] = ability_json[ABILITY_TYPES[a]]

    def to_dict(self) -> dict:
        return self._abilities
