import time
from random import randint

from hurby.twitch.irc import irc_chat_extractor
from hurby.twitch.irc.threads.hurby_thread import HurbyThread
from hurby.utils import logger
from hurby.utils.const import CONST


class CronJobs(HurbyThread):
    def __init__(self, tw_conf, receiver, irc):
        HurbyThread.__init__(self)
        self.twitch_conf = tw_conf
        self.receiver = receiver
        self.irc = irc
        self.issued_jobs = [False] * len(self.twitch_conf.cron_jobs)

    def run(self):
        logger.log(logger.INFO, "Running CronJobs")
        while CONST.RUNNING:
            logger.log(logger.INFO, "Do cron job")
            cmd = self.twitch_conf.cron_jobs[self._rand_job()]
            tmp = irc_chat_extractor.extract_command(cmd)
            self.receiver.do_command(tmp, None, self.irc)
            time.sleep(self.twitch_conf.cron_job_time * 60)
        logger.log(logger.INFO, "Stopped cron jobs")

    def _rand_job(self):
        if self._check_if_all_jobs_where_triggered():
            logger.log(logger.INFO, "All jobs issued, resetting...")
            self._reset_all_jobs()
        job_id = randint(0, len(self.twitch_conf.cron_jobs) - 1)
        while self.issued_jobs[job_id]:
            job_id = randint(0, len(self.twitch_conf.cron_jobs) - 1)
        self.issued_jobs[job_id] = True
        return job_id

    def _check_if_all_jobs_where_triggered(self):
        for i in range(0, len(self.issued_jobs)):
            if not self.issued_jobs[i]:
                return False
        return True

    def _reset_all_jobs(self):
        for i in range(0, len(self.issued_jobs)):
            self.issued_jobs[i] = False
