from config import Config
from utils import Const, Logger


def loadModules(modules):
    configFile = "none"
    for i in range(0, len(modules)):
        if modules[Config.MODULE_TWITCH] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITCH
        elif modules[Config.MODULE_PATREON] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_PATREON
        elif modules[Config.MODULE_STEAM] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_STEAM
        elif modules[Config.MODULE_TRELLO] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TRELLO
        elif modules[Config.MODULE_TWITTER] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITTER
        elif modules[Config.MODULE_YOUTUBE] == "enabled":
            Logger.log(Logger.INFO, "Loading Twitch config")
            configFile = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_YOUTUBE
        else:
            Logger.log(Logger.INFO, "Unknown module at position: "+i)
