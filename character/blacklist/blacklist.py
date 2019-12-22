import time

from character.blacklist.external_blacklist_updater import BlacklistUpdater
from character.user_id_types import UserIDType
from utils import json_loader, logger
from utils.const import CONST


class Blacklist:
    DIR_CHARACTER = CONST.DIR_APP_DATA_ABSOLUTE + "/characters"
    BLACKLIST_FILE = DIR_CHARACTER + "/" + CONST.FILE_BLACKLIST

    def __init__(self, hurby):
        self.blacklist_updater = BlacklistUpdater(self)
        self.hurby = hurby
        self.last_external_banlist_update = 0
        self.update_external_banlist_every_days = 7
        self.external_banlist_json = "https://raw.githubusercontent.com/tarumes/twitch-ban-list/master/public_ban.json"
        self.twitch_names = []
        self.twitch_ids = []
        self.youtube_ids = []
        self.mails = []
        try:
            f = open(Blacklist.BLACKLIST_FILE)
            blacklist_json = json_loader.load_json(Blacklist.BLACKLIST_FILE)
            self.twitch_names = blacklist_json["twitch_names"]
            self.twitch_ids = blacklist_json["twitch_ids"]
            self.youtube_ids = blacklist_json["youtube_ids"]
            self.mails = blacklist_json["mails"]
            self.last_external_banlist_update = blacklist_json["last_external_banlist_update"]
            self.update_external_banlist_every_days = blacklist_json["update_external_banlist_every_days"]
            self.external_banlist_json = blacklist_json["external_banlist_json"]
        except IOError:
            self.save()

    def init(self):
        if self._external_ban_list_need_update():
            logger.log(logger.DEV, "External Banlist outdated.")
            logger.log(logger.DEV, "Start BlacklistUpdater Thread")
            self.blacklist_updater.start()
            logger.log(logger.DEV, "Started BlacklistUpdater Thread, now running...")

    def is_name_blacklisted(self, user_name, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            return user_name in self.twitch_names
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False

    def is_id_blacklisted(self, user_id, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            return user_id in self.twitch_ids
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False

    def clear_blacklisted_character_files(self):
        for name in self.twitch_names:
            self.hurby.char_manager.delete_character(name, UserIDType.TWITCH)

    def save(self):
        logger.log(logger.DEV, "Saving Blacklist")
        blacklist_dict = {
            "last_external_banlist_update": self.last_external_banlist_update,
            "update_external_banlist_every_days": self.update_external_banlist_every_days,
            "external_banlist_json":self.external_banlist_json,
            "twitch_names": self.twitch_names,
            "twitch_ids": self.twitch_ids,
            "youtube_ids": self.youtube_ids,
            "mails": self.mails
        }
        json_loader.save_json(Blacklist.BLACKLIST_FILE, blacklist_dict)

    def external_ban_list_updated_now(self):
        self.last_external_banlist_update = time.time()
        self.save()

    def _external_ban_list_need_update(self):
        refresh_days_in_seconds = self.update_external_banlist_every_days*60*60*24
        time_diff = time.time() - self.last_external_banlist_update
        return time_diff >= refresh_days_in_seconds
