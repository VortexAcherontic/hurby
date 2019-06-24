class BotConfig:
    MODULE_TWITCH = 0
    MODULE_TWITTER = 1
    MODULE_YOUTUBE = 2
    MODULE_PATREON = 3
    MODULE_STEAM = 4
    MODULE_TRELLO = 5
    MODULE_MINIGAME = 6

    def __init__(self, botJSON):
        self.botname = botJSON["botname"]
        self.modules = [None] * 7
        self.modules[BotConfig.MODULE_TWITCH] = botJSON["modules"]["twitch"]
        self.modules[BotConfig.MODULE_TWITTER] = botJSON["modules"]["twitter"]
        self.modules[BotConfig.MODULE_YOUTUBE] = botJSON["modules"]["youtube"]
        self.modules[BotConfig.MODULE_PATREON] = botJSON["modules"]["patreon"]
        self.modules[BotConfig.MODULE_STEAM] = botJSON["modules"]["steam"]
        self.modules[BotConfig.MODULE_TRELLO] = botJSON["modules"]["trello"]
        self.modules[BotConfig.MODULE_MINIGAME] = botJSON["modules"]["minigame"]
