from hurby import Hurby
from twitch_hurby.twitch_irc_bot import TwitchIRCBot
from utils import logger

logger.log(logger.INFO, "Starting Bot...")

hurby = Hurby()
# hurby.get_twitch_receiver().do_command("!hurby", None, None)
# hurby.get_twitch_receiver().do_command("!help", None, None)

if hurby.get_char_manager().get_black_list().is_black_listed("Penis"):
    pass
    # logger.log(logger.INFO, "Penis is blacklisted")

if not hurby.get_char_manager().get_black_list().is_black_listed("Suroth"):
    pass
    # logger.log(logger.INFO, "Suroth is not blacklisted")

# hurby.get_twitch_receiver().do_command("!loots", None, None)
irc_listener = hurby.get_twitch_receiver().get_irc_listener().start()
# irc_listener.handle_forever()
# hurby.get_twitch_receiver().get_irc_listener().run()
