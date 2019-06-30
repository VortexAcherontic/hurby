import time
from random import randint

from twitch_hurby.irc import irc_chat_extractor
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class CronJobs (HurbyThread):
    def __init__(self, tw_conf, receiver, irc):
        HurbyThread.__init__(self)
        self.twitch_conf = tw_conf
        self.receiver = receiver
        self.irc = irc

    def run(self):
        logger.log(logger.INFO, "Running CronJobs")
        while CONST.RUNNING:
            logger.log(logger.INFO, "Do cron job")
            cmd = self.twitch_conf.cron_jobs[randint(0, len(self.twitch_conf.cron_jobs) - 1)]
            tmp = irc_chat_extractor.extract_command(cmd)
            self.receiver.do_command(tmp, None, self.irc)
            time.sleep(self.twitch_conf.cron_job_time * 60)
        logger.log(logger.INFO, "Stopped cron jobs")
