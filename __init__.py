from config.Config import Config
from utils import JSONLoader, Const, Logger



Logger.log(Logger.INFO, "Starting Bot...")

configFileBot = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_HURBY

jsonBotConfig = JSONLoader.loadJSON(configFileBot)

botConfig = Config(jsonBotConfig, "none")