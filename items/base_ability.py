ABILITY_TYPES = {
    "BLIND": "blind"
}


class BaseAbility:
    def __init__(self, ability_json):
        self.abilities = {}
        for a in ABILITY_TYPES:
            if ABILITY_TYPES[a] in ability_json:
                self.abilities[a] = ability_json[ABILITY_TYPES[a]]
