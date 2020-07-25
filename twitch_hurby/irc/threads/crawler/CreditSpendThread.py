import time

from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class CreditSpendThread(HurbyThread):
    def __init__(self, crawler):
        HurbyThread.__init__(self)
        self.crawler = crawler
        self.spend_time = self.crawler.spend_time

    def run(self):
        logger.log(logger.INFO, "Running spend Thread...")
        while CONST.RUNNING:
            time.sleep(self.spend_time * 60)
            logger.log(logger.INFO, "Spending credits ...")
            if self.crawler.char_man.chars is not None:
                for c in self.crawler.char_man.chars:
                    if c is not None:
                        if c.is_supporter:
                            c.add_credits(self.crawler.credit_increase_supporter)
                        else:
                            c.add_credits(self.crawler.credit_increase_base)
                        c.save()
            else:
                logger.log(logger.INFO, "No Chars :/")
