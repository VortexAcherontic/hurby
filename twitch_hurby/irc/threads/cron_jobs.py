import threading
import time
from random import randint

from utils import logger


class CronJobs (threading.Thread):
    def __init__(self, tw_conf, receiver, irc):
        threading.Thread.__init__(self)
        self.twitch_conf = tw_conf
        self.receiver = receiver
        self.irc = irc

    def run(self):
        logger.log(logger.INFO, "Running CronJobs")
        while True:
            logger.log(logger.INFO, "Do cron job")
            cmd = self.twitch_conf.cron_jobs[randint(0, len(self.twitch_conf.cron_jobs) - 1)]
            self.receiver.do_command(cmd, None, None, self.irc)
            time.sleep(self.twitch_conf.cron_job_time * 60)
