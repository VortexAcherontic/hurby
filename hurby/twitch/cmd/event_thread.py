import random
import time

from hurby.twitch.irc.threads.hurby_thread import HurbyThread
from hurby.utils import logger
from hurby.utils.const import CONST


class EventThread(HurbyThread):
    def __init__(self, hurby, events):
        HurbyThread.__init__(self)
        self.hurby = hurby
        self.events = events

    def run(self):
        logger.log(logger.DEV, "Started event thread...")
        bot_cfg = self.hurby.botConfig
        min_min = bot_cfg.event_cooldown_min_min
        max_min = bot_cfg.event_cooldown_max_min
        sleep_time = random.randint(min_min, max_min)
        if CONST.DEVMODE:
            sleep_time = 1
        while CONST.RUNNING:
            logger.log(logger.INFO, "Event Thread sleep for " + str(sleep_time) + " mins")
            time.sleep(sleep_time * 60)
            logger.log(logger.INFO, "Tick event")
            rnd_event = self.events[random.randint(0, len(self.events) - 1)]
            rnd_event.issue_event()
