import json

from utils import Const, JSONLoader


class Config:
    def __init__(self, botJSON, tiwtchJSON):
        self.botname = botJSON["botname"]
        print("Bot Name: " + self.botname)