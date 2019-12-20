import os
import random
import time

from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class EventThread(HurbyThread):
    def __init__(self, hurby, events):
        HurbyThread.__init__(self)
        self.hurby = hurby
        self.events = events

    def run(self):
        logger.log(logger.DEV, "Started event thread...")
        bot_cfg = self.hurby.get_bot_config()
        min_min = bot_cfg.event_cooldown_min_min
        max_min = bot_cfg.event_cooldown_max_min
        if int(os.environ["HURBY_DEVMODE"]) == 1:
            sleep_time = 1
        else:
            sleep_time = random.randint(min_min, max_min)
        while CONST.RUNNING:
            logger.log(logger.INFO, "Event Thread sleep for " + str(sleep_time) + " mins")
            time.sleep(sleep_time * 60)
            logger.log(logger.INFO, "Tick event")
            rnd_event = self.events[random.randint(0, len(self.events) - 1)]
            rnd_event.issue_event()
            if int(os.environ["HURBY_DEVMODE"]) == 1:
                sleep_time = 1
            else:
                sleep_time = random.randint(min_min, max_min)
