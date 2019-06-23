import json

from utils import Const, JSONLoader

MODULE_TWITCH = 0
MODULE_TWITTER = 1
MODULE_YOUTUBE = 2
MODULE_PATREON = 3
MODULE_STEAM = 4
MODULE_TRELLO = 5


class Config:
    def __init__(self, botJSON, twitchJSON):
        self.botname = botJSON["botname"]
        self.modules = [None] * 6
        self.modules[MODULE_TWITCH] = botJSON["modules"]["twitch"]
        self.modules[MODULE_TWITTER] = botJSON["modules"]["twitter"]
        self.modules[MODULE_YOUTUBE] = botJSON["modules"]["youtube"]
        self.modules[MODULE_PATREON] = botJSON["modules"]["patreon"]
        self.modules[MODULE_STEAM] = botJSON["modules"]["steam"]
        self.modules[MODULE_TRELLO] = botJSON["modules"]["trello"]