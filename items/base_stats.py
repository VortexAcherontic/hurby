STATS_TYPES = {
    "VISION": "vision",
    "ENDURANCE": "endurance",
    "AMOUR": "amour",
    "LUCK": "luck"
}


class BaseStats:
    def __init__(self, stats_json):
        self._stats = {}
        for s in STATS_TYPES:
            if STATS_TYPES[s] in stats_json:
                self._stats[s] = stats_json[STATS_TYPES[s]]

    def to_dict(self) -> dict:
        return self._stats
