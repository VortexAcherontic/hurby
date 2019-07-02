from hurby import Hurby
from utils import logger

logger.log(logger.INFO, "Starting Bot...")

hurby = Hurby()
irc_channel = hurby.twitch_receiver.twitch_conf.channel_name
irc_listener = hurby.get_twitch_receiver().get_twitch_irc_connector().start(irc_channel)
