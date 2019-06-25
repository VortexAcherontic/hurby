from config.bot_config import BotConfig
from twitch_hurby.cmd import cmd_const, simple_response
from utils import logger


class CMDLoader:
    def __init__(self):
        pass

    def create_cmd(self, json, bot_config: BotConfig):
        if json["type"] == cmd_const.CMDConst.TYPE_REPLY:
            # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is SimpleReply")
            simpleCMD = simple_response.SimpleResponse(json)
            return simpleCMD
        elif json["type"] == cmd_const.CMDConst.TYPE_ACTION:
            if json["minigame"]:
                if bot_config.modules[bot_config.MODULE_MINIGAME] == "enabled":
                    pass
                    # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is Mini game")
                else:
                    pass
                    # Logger.log(Logger.INFO, "Skip mini game: " + json["cmd"] + " mini games are disabled")
            else:
                pass
                # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is ActionCommand")
        else:
            logger.log(logger.INFO, "Unknown command type: " + json["type"] + " for command: " + json["cmd"])
