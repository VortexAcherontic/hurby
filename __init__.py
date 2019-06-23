from Hurby import Hurby
from config.BotConfig import BotConfig
from utils import JSONLoader, Const, Logger, ModuleLoader

Logger.log(Logger.INFO, "Starting Bot...")

configFileBot = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_HURBY
jsonBotConfig = JSONLoader.loadJSON(configFileBot)
botConfig = BotConfig(jsonBotConfig)

hurby = Hurby(botConfig)

if hurby.botConfig.modules[BotConfig.MODULE_TWITCH] == "enabled":
    Logger.log(Logger.INFO, "Twitch enabled")