import time

from character.blacklist import blacklist_crawler
from character.user_id_types import UserIDType
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.time_measure import TimeMeasure


class BlacklistUpdater(HurbyThread):
    def __init__(self, blacklist):
        HurbyThread.__init__(self)
        self.blacklist = blacklist
        self.last_save_time = time.time()

    def run(self):
        self._update_from_external()

    def _update_from_external(self):
        tm = TimeMeasure()
        bots = blacklist_crawler.get_twitch_bot_names()
        for bot_name in bots["names"]:
            if not self.blacklist.is_name_blacklisted(bot_name, UserIDType.TWITCH):
                self.blacklist.twitch_names.append(bot_name)
                self._save_every_minute()
        for bot_id in bots["ids"]:
            if not self.blacklist.is_id_blacklisted(bot_id, UserIDType.TWITCH):
                self.blacklist.twitch_ids.append(bot_id)
                self._save_every_minute()
        self.blacklist.save()
        self.blacklist.clear_blacklisted_character_files()
        end = tm.end()
        logger.log(logger.DEV, "Parsing external Blacklist took: " + end + "s")

    def _save_every_minute(self):
        if time.time() - self.last_save_time >= 60:
            self.blacklist.save()
            self.last_save_time = time.time()
