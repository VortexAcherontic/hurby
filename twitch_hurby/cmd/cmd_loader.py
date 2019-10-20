from config.bot_config import BotConfig
from twitch_hurby.cmd import simple_response
from twitch_hurby.cmd.actions.add_credits import AddCreditsCommand
from twitch_hurby.cmd.actions.credits_command import CreditsCommand
from twitch_hurby.cmd.actions.gift_credits import GiftCreditsCommand
from twitch_hurby.cmd.actions.help_command import HelpCommand
from twitch_hurby.cmd.actions.items.inventory import InventoryCommand
from twitch_hurby.cmd.actions.items.spawn_item import SpawnItemCommand
from twitch_hurby.cmd.actions.raid_command import RaidCommand
from twitch_hurby.cmd.actions.search_command import SearchCommand
from twitch_hurby.cmd.actions.set_credits_command import SetCreditsCommand
from twitch_hurby.cmd.actions.shutdown_command import ShutdownCommand
from twitch_hurby.cmd.actions.whisper_command import WhisperCommand
from twitch_hurby.cmd.enums.cmd_types import CMDType
from utils import logger


def create_cmd(json_data, bot_config: BotConfig, hurby):
    cmd_type = CMDType(json_data["type"])

    if cmd_type == CMDType.REPLY:
        # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is SimpleReply")
        simple_cmd = simple_response.SimpleResponse(json_data, hurby)
        return simple_cmd
    elif cmd_type == CMDType.ACTION:
        logic_trigger = json_data["reply"]
        if json_data["minigame"]:
            if bot_config.modules[bot_config.MODULE_MINIGAME]:
                if logic_trigger == "$raid":
                    return RaidCommand(json_data, hurby)
                if logic_trigger == "$spawn_item":
                    return SpawnItemCommand(json_data, hurby)
                if logic_trigger == "$inventory":
                    return InventoryCommand(json_data, hurby)
            else:
                pass
                # Logger.log(Logger.INFO, "Skip mini game: " + json["cmd"] + " mini games are disabled")
        else:
            if logic_trigger == "$search":
                return SearchCommand(json_data, hurby)
            if logic_trigger == "$whisper":
                return WhisperCommand(json_data, hurby)
            if logic_trigger == "$shutdown":
                return ShutdownCommand(json_data, hurby)
            if logic_trigger == "$credits":
                return CreditsCommand(json_data, hurby)
            if logic_trigger == "$set_credits":
                return SetCreditsCommand(json_data, hurby)
            if logic_trigger == "$help":
                return HelpCommand(json_data, hurby)
            if logic_trigger == "$giftcredits":
                return GiftCreditsCommand(json_data, hurby)
            if logic_trigger == "$add_credits":
                return AddCreditsCommand(json_data, hurby)

    else:
        logger.log(logger.INFO, "Unknown command type: " + json_data["type"] + " for command: " + json_data["cmd"])
