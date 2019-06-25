from character.CharacterManager import CharacterManager
from config.BotConfig import BotConfig
from twitch.TwitchReciever import TwitchReceiver
from utils import Logger


class Hurby:

    def __init__(self):
        self.botConfig = BotConfig()
        self.char_Manager = CharacterManager()
        self.twitch_receiver = None
        self.load_modules()

    def get_char_manager(self):
        return self.char_Manager

    def load_modules(self):
        if self.botConfig.modules[BotConfig.MODULE_MINIGAME] == "enabled":
            Logger.log(Logger.INFO, "Module Mini games: enabled")
        if self.botConfig.modules[BotConfig.MODULE_TWITCH] == "enabled":
            Logger.log(Logger.INFO, "Module Twitch: enabled")
            self.twitch_receiver = TwitchReceiver(self)

    def get_twitch_receiver(self):
        return self.twitch_receiver

    def get_bot_config(self):
        return self.botConfig
