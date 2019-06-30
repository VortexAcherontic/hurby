from config.bot_config import BotConfig
from twitch_hurby.cmd import simple_response
from twitch_hurby.cmd.enums.cmd_types import CMDType
from utils import logger


class CMDLoader:
    def __init__(self):
        pass

    def create_cmd(self, json_data, bot_config: BotConfig, irc_connector):
        cmd_type = CMDType(json_data["type"])

        if cmd_type == CMDType.REPLY:
            # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is SimpleReply")
            simpleCMD = simple_response.SimpleResponse(json_data, irc_connector)
            return simpleCMD
        elif cmd_type == CMDType.ACTION:
            if json_data["minigame"]:
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
            logger.log(logger.INFO, "Unknown command type: " + json_data["type"] + " for command: " + json_data["cmd"])
