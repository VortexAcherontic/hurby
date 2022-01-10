from hurby.character.character_manager import CharacterManager
from hurby.config.bot_config import BotConfig
from hurby.items.item_manager import ItemManager
from hurby.modules.lottery.lottery_manager import LotteryManager
from hurby.twitch.minigame.loots import Loots
from hurby.twitch.twitch_receiver import TwitchReceiver
from hurby.utils.api_test import test_api


class HurbyMain:

    def __init__(self):
        self.botConfig = BotConfig()
        self.char_manager: CharacterManager = CharacterManager(self)
        if self.botConfig.modules[BotConfig.MODULE_LOTTERY]:
            self.lottery_manager = LotteryManager(self)
        if self.botConfig.modules[BotConfig.MODULE_TWITCH]:
            self.twitch_receiver = TwitchReceiver(self)
            self.loots = Loots(self.char_manager, self.twitch_receiver.twitch_listener)
            self.twitch_receiver.twitch_conf.load_cmds()
            self.twitch_receiver.twitch_conf.load_events()
        self.item_manager = ItemManager()
        test_api(self)

    def get_twitch_receiver(self) -> TwitchReceiver:
        return self.twitch_receiver

    def get_bot_config(self) -> BotConfig:
        return self.botConfig