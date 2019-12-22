from hurby import Hurby
from utils import logger

logger.log(logger.INFO, "Starting Bot...")

hurby = Hurby()
irc_channels = hurby.twitch_receiver.twitch_conf.channel_names
hurby.get_twitch_receiver().get_twitch_irc_connector().start(irc_channels)
hurby.char_manager.black_list.init()
