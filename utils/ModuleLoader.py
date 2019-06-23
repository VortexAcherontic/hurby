from config import BotConfig
from twitch import TwitchConfig
from utils import Const, Logger, JSONLoader


class ModuleLoader:
    def load_modules(modules, hurby):
        configFile = "none"
        for i in range(0, len(modules)):
            if modules[BotConfig.MODULE_TWITCH] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITCH
                twitchJSON = JSONLoader.loadJSON(configFile)
                hurby.twitchConf = TwitchConfig.TwitchConfig.configure(hurby.twitchConf, twitchJSON)
            elif modules[BotConfig.MODULE_PATREON] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_PATREON
            elif modules[BotConfig.MODULE_STEAM] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_STEAM
            elif modules[BotConfig.MODULE_TRELLO] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TRELLO
            elif modules[BotConfig.MODULE_TWITTER] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITTER
            elif modules[BotConfig.MODULE_YOUTUBE] == "enabled":
                Logger.log(Logger.INFO, "Loading Twitch config")
                configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_YOUTUBE
            else:
                Logger.log(Logger.INFO, "Unknown module at position: "+i)
