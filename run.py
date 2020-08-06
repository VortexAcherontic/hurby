from config.bot_config import BotConfig
from hurby import Hurby
from utils import logger
from webapp.app import run_flask

try:
    logger.log(logger.INFO, "Starting Bot...")

    hurby = Hurby()
    irc_channels = hurby.twitch_receiver.twitch_conf.channel_names
    hurby.get_twitch_receiver().get_twitch_irc_connector().start(irc_channels)
    hurby.char_manager.black_list.init()
    if hurby.botConfig.modules[BotConfig.MODULE_WEBSERVER]:
        logger.log(logger.INFO, "Starting flask server...")
        run_flask(hurby)
except Exception as e:
    logger.log(logger.FATAL, str(e))
