from config.Config import Config
from utils import JSONLoader, Const

configPath = Const.CONST.USER_HOME + "/" + Const.CONST.DIR_APP_DATA + "/" + Const.CONST.DIR_CONF

configFileBot = configPath + "/" + Const.CONST.FILE_CONF_HURBY
configFileTwitch = configPath + "/" + Const.CONST.FILE_CONF_HURBY

jsonBotConfig = JSONLoader.loadJSON(configFileBot)

botConfig = Config(jsonBotConfig, "none")