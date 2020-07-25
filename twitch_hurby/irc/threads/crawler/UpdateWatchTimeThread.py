import time

from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class UpdateWatchTimeThread(HurbyThread):
    def __init__(self, crawler):
        super().__init__()
        self.crawler = crawler

    def run(self):
        logger.log(logger.INFO, "Running watchtime thread...")
        while CONST.RUNNING:
            time.sleep(60)
            logger.log(logger.INFO, "Add watchtime...")
            if self.crawler.char_man.chars is not None:
                for character in self.crawler.char_man.chars:
                    if character is not None:
                        character.update_watchtime()