from character.character_manager import CharacterManager
from config.bot_config import BotConfig
from items.item_manager import ItemManager
from twitch_hurby.minigame.loots import Loots
from twitch_hurby.twitch_receiver import TwitchReceiver

from utils import logger


class Hurby:

    def __init__(self):
        self.botConfig = BotConfig()
        self.char_manager: CharacterManager = CharacterManager(self)
        self.twitch_receiver = None
        self.load_modules()
        self.loots = Loots(self.char_manager, self.twitch_receiver)
        self.item_manager = ItemManager()

    def load_modules(self):
        if self.botConfig.modules[BotConfig.MODULE_MINIGAME]:
            logger.log(logger.INFO, "Module Mini games: enabled")
        if self.botConfig.modules[BotConfig.MODULE_TWITCH]:
            logger.log(logger.INFO, "Module Twitch: enabled")
            self.twitch_receiver = TwitchReceiver(self)

    def get_twitch_receiver(self) -> TwitchReceiver:
        return self.twitch_receiver

    def get_bot_config(self) -> BotConfig:
        return self.botConfig
