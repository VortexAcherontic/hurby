from enum import Enum


class UserIDType(Enum):
    TWITCH = "twitch"
    YOUTUBE = "yt"
    TWITTER = "twitter"
    PATREON = "patreon"
    TELEGRAM = "telegram"
    STEAM = "steam"
    DISCORD = "discord"