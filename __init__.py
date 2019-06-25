from Hurby import Hurby
from utils import Logger

Logger.log(Logger.INFO, "Starting Bot...")

hurby = Hurby()
hurby.get_twitch_receiver().do_command("!hurby", None, None)
hurby.get_twitch_receiver().do_command("!help", None, None)

if hurby.get_char_manager().get_black_list().is_black_listed("Penis"):
    Logger.log(Logger.INFO, "Penis is blacklisted")

if not hurby.get_char_manager().get_black_list().is_black_listed("Suroth"):
    Logger.log(Logger.INFO, "Suroth is not blacklisted")


hurby.get_twitch_receiver().do_command("!loots", None, None)