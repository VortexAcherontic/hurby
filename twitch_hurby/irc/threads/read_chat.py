import threading
import time

from utils import logger


class ReadChat (threading.Thread):
    def __init__(self, irc_con, tick):
        threading.Thread.__init__(self)
        self.irc = irc_con
        self.tick = tick

    def run(self):
        logger.log(logger.INFO, "Running ReadChat")
        while True:
            time.sleep(self.tick)
            self.irc.read_chat()
