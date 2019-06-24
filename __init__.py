from Hurby import Hurby
from config.BotConfig import BotConfig
from twitch import TwitchConfig
from twitch.TwitchReciever import TwitchReciver
from utils import JSONLoader, Const, Logger

Logger.log(Logger.INFO, "Starting Bot...")

configFileBot = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_HURBY
jsonBotConfig = JSONLoader.loadJSON(configFileBot)
botConfig = BotConfig(jsonBotConfig)

hurby = Hurby(botConfig)
twitch_receiver = None

if hurby.botConfig.modules[BotConfig.MODULE_MINIGAME] == "enabled":
    Logger.log(Logger.INFO, "Mini games enabled")

if hurby.botConfig.modules[BotConfig.MODULE_TWITCH] == "enabled":
    Logger.log(Logger.INFO, "Twitch enabled")
    configFileTwitch = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITCH
    twitchJSON = JSONLoader.loadJSON(configFileTwitch)
    twitchConf = TwitchConfig.TwitchConfig(twitchJSON, hurby.botConfig)
    twitch_receiver = TwitchReciver(twitchConf)
    twitch_receiver.do_command("!hurby", None, None)
