from character.character_manager import CharacterManager
from config.bot_config import BotConfig
from items.item_manager import ItemManager
from twitch_hurby.minigame.loots import Loots
from twitch_hurby.twitch_receiver import TwitchReceiver


class Hurby:

    def __init__(self):
        self.botConfig = BotConfig()
        self.char_manager: CharacterManager = CharacterManager(self)
        if self.botConfig.modules[BotConfig.MODULE_TWITCH]:
            self.twitch_receiver = TwitchReceiver(self)
            self.loots = Loots(self.char_manager, self.twitch_receiver.twitch_listener)
            self.twitch_receiver.twitch_conf.load_cmds()
            self.twitch_receiver.twitch_conf.load_events()
        self.item_manager = ItemManager()

    def get_twitch_receiver(self) -> TwitchReceiver:
        return self.twitch_receiver

    def get_bot_config(self) -> BotConfig:
        return self.botConfig
