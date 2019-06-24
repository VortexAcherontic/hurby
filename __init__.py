from Hurby import Hurby
from character.Blacklist import Blacklist
from config.BotConfig import BotConfig
from twitch import TwitchConfig
from twitch.TwitchReciever import TwitchReceiver
from utils import JSONLoader, Const, Logger

Logger.log(Logger.INFO, "Starting Bot...")

configFileBot = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_HURBY
jsonBotConfig = JSONLoader.loadJSON(configFileBot)
botConfig = BotConfig(jsonBotConfig)

hurby = Hurby(botConfig)
blacklist = Blacklist()
twitch_receiver = None

if hurby.botConfig.modules[BotConfig.MODULE_MINIGAME] == "enabled":
    Logger.log(Logger.INFO, "Mini games enabled")

if hurby.botConfig.modules[BotConfig.MODULE_TWITCH] == "enabled":
    Logger.log(Logger.INFO, "Twitch enabled")
    configFileTwitch = Const.CONST.DIR_CONF_ABSOLUTE + "/" + Const.CONST.FILE_CONF_TWITCH
    twitchJSON = JSONLoader.loadJSON(configFileTwitch)
    twitchConf = TwitchConfig.TwitchConfig(twitchJSON, hurby.botConfig)
    twitch_receiver = TwitchReceiver(twitchConf)
    twitch_receiver.do_command("!hurby", None, None)
    twitch_receiver.do_command("!help", None, None)

if blacklist.is_black_listed("Penis"):
    Logger.log(Logger.INFO, "Penis is blacklisted")

if not blacklist.is_black_listed("Suroth"):
    Logger.log(Logger.INFO, "Suroth is not blacklisted")
