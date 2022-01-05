import time

from twitch_hurby.helix.is_streamer_live import is_stream_live
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class UpdateWatchTimeThread(HurbyThread):
    def __init__(self, crawler, twitch_config):
        super().__init__()
        self.crawler = crawler
        self.twitch_config = twitch_config

    def run(self):
        logger.log(logger.INFO, "Running watchtime thread...")
        while CONST.RUNNING:
            time.sleep(60)
            if is_stream_live(self.twitch_config.streamer, self.twitch_config):
                logger.log(logger.INFO, "Add watchtime...")
                if self.crawler.char_man.chars is not None:
                    for character in self.crawler.char_man.chars:
                        if character is not None:
                            character.update_watchtime()
            else:
                logger.log(logger.DEV, "Not updating watchtime, Stream offline")