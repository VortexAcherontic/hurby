from enum import Enum


class ChatterType(Enum):
    BROADCASTER = "broadcaster"
    VIP = "vips"
    MODERATOR = "moderators"
    STAFF = "staff"
    ADMINS = "admins"
    GLOBAL_MODERATORS = "global_mods"
    VIEWER = "viewers"
