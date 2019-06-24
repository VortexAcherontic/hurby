from config import BotConfig
from twitch.cmd import CMDConst, SimpleResponse
from utils import Logger


class CMDLoader:
    def __init__(self):
        pass

    def create_cmd(self, json, bot_config):
        if json["type"] == CMDConst.CMDConst.TYPE_REPLY:
            # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is SimpleReply")
            simpleCMD = SimpleResponse.SimpleResponse(json)
            return simpleCMD
        elif json["type"] == CMDConst.CMDConst.TYPE_ACTION:
            if json["minigame"]:
                if bot_config.modules[BotConfig.BotConfig.MODULE_MINIGAME] == "enabled":
                    pass
                    # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is Mini game")
                else:
                    pass
                    # Logger.log(Logger.INFO, "Skip mini game: " + json["cmd"] + " mini games are disabled")
            else:
                pass
                # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is ActionCommand")
        else:
            Logger.log(Logger.INFO, "Unknown command type: " + json["type"] + " for command: " + json["cmd"])
