import math
import threading
import time

from character.blacklist import blacklist_crawler
from character.user_id_types import UserIDType
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.time_measure import TimeMeasure

BLACK_LOCK = threading.Lock()


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

        name_parser_threads = []
        offset = 0
        steps = math.ceil(len(bots["names"]) / self.blacklist.updater_threads)
        for i in range(0, int(self.blacklist.updater_threads / 2)):
            dict_start = offset
            dict_end = offset + steps
            parser_list = bots["names"][dict_start:dict_end]
            offset = offset + steps
            name_parser_threads.append(BlackParserThread(parser_list, True, self))
        for thread in name_parser_threads:
            thread.start()

        id_parser_threads = []
        offset = 0
        steps = math.ceil(len(bots["ids"]) / self.blacklist.updater_threads)
        for i in range(0, int(self.blacklist.updater_threads / 2)):
            dict_start = offset
            dict_end = offset + steps
            parser_list = bots["ids"][dict_start:dict_end]
            offset = offset + steps
            id_parser_threads.append(BlackParserThread(parser_list, False, self))
        for thread in id_parser_threads:
            thread.start()

        self.blacklist.save()
        self.blacklist.clear_blacklisted_character_files()
        end = tm.end()
        logger.log(logger.DEV, "Parsing external Blacklist took: " + str(end) + "s")

    def save_every_minute(self):
        if time.time() - self.last_save_time >= 60:
            self.blacklist.save()
            self.last_save_time = time.time()


class BlackParserThread(HurbyThread):
    def __init__(self, sub_ban_dict: list, check_names: bool, black_updater):
        HurbyThread.__init__(self)
        self.ban_dict = sub_ban_dict
        self.check_names = check_names
        self.black_updater = black_updater

    def run(self):
        for tmp in self.ban_dict:
            if self.check_names:
                if not self._is_name_blacklisted(tmp, UserIDType.TWITCH):
                    BLACK_LOCK.acquire()
                    self.black_updater.blacklist.twitch_names.append(tmp)
                    self.black_updater.save_every_minute()
                    BLACK_LOCK.release()
            else:
                if not self.black_updater.blacklist.is_id_blacklisted(tmp, UserIDType.TWITCH):
                    BLACK_LOCK.acquire()
                    self.black_updater.blacklist.twitch_ids.append(tmp)
                    self.black_updater.save_every_minute()
                    BLACK_LOCK.release()

    def _is_name_blacklisted(self, user_name, user_id_type: UserIDType):
        black_list_dict = self.black_updater.blacklist.twitch_ids.copy()
        if user_id_type == UserIDType.TWITCH:
            for i in black_list_dict:
                if i == user_name:
                    return True
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False

    def _is_id_blacklisted(self, user_id, user_id_type: UserIDType):
        black_list_dict = self.black_updater.blacklist.twitch_ids.copy()
        if user_id_type == UserIDType.TWITCH:
            for i in black_list_dict:
                if i == user_id:
                    return True
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False
