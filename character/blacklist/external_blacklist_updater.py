import time

from character.blacklist import blacklist_crawler
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger, hurby_utils
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
        bots = blacklist_crawler.get_twitch_bot_names(self.blacklist.external_banlist_json)
        if bots is not None:
            for bot_name in bots["names"]:
                self.blacklist.twitch_names.append(bot_name)
            for bot_id in bots["ids"]:
                self.blacklist.twitch_ids.append(bot_id)

            self.blacklist.twitch_names = hurby_utils.remove_doubles_from_list(self.blacklist.twitch_names)
            self.blacklist.twitch_ids = hurby_utils.remove_doubles_from_list(self.blacklist.twitch_ids)
            self.blacklist.external_ban_list_updated_now()
            self.blacklist.save()
            self.blacklist.clear_blacklisted_character_files()
            blacklist_crawler.delete_tmp_file()
            end = tm.end()
            logger.log(logger.DEV, "Parsing external Blacklist took: " + str(end) + "s")

    def _save_every_minute(self):
        if time.time() - self.last_save_time >= 60:
            self.blacklist.save()
            self.last_save_time = time.time()
