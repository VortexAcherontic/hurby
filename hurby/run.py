from traceback import print_exc

from hurby.main import HurbyMain
from hurby.utils import logger

try:
    logger.log(logger.INFO, "Starting Bot...")

    hurby = HurbyMain()
    irc_channels = hurby.twitch_receiver.twitch_conf.channel_names
    hurby.twitch_receiver.get_twitch_irc_connector().start(irc_channels)
    hurby.char_manager.black_list.init()
except Exception as e:
    logger.log(logger.FATAL, str(e))
    logger.log(logger.FATAL, print_exc(e))
