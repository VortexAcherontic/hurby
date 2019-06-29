from hurby import Hurby
from utils import logger

logger.log(logger.INFO, "Starting Bot...")

hurby = Hurby()
irc_listener = hurby.get_twitch_receiver().get_twitch_irc_connector().start("#couchrebellen")
