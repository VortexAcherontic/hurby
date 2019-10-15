EFFECT_TYPES = {
    "VISION": "vision",
    "ENDURANCE": "endurance",
    "AMOUR": "amour",
    "LUCK": "luck"
}


class BaseEffect:
    def __init__(self, effect_json):
        self.effects = {}
        for e in EFFECT_TYPES:
            if EFFECT_TYPES[e] in effect_json:
                self.effects[e] = effect_json[EFFECT_TYPES[e]]