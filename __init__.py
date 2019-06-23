from Hurby import Hurby
from config.BotConfig import Config
from utils import JSONLoader, Const, Logger, ModuleLoader

configFileBot = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_HURBY
jsonBotConfig = JSONLoader.loadJSON(configFileBot)
botConfig = Config(jsonBotConfig, "none")

hurby = Hurby()
modLoader = ModuleLoader()

Logger.log(Logger.INFO, "Starting Bot...")



ModuleLoader.ModuleLoader.load_modules(botConfig.modules, hurby)
