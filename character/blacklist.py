from character import blacklist_crawler
from character.user_id_types import UserIDType
from utils import json_loader, logger
from utils.const import CONST
from utils.time_measure import TimeMeasure


class Blacklist:
    DIR_CHARACTER = CONST.DIR_APP_DATA_ABSOLUTE + "/characters"
    BLACKLIST_FILE = DIR_CHARACTER + "/" + CONST.FILE_BLACKLIST

    def __init__(self, hurby):
        self.hurby = hurby
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
        except IOError:
            self._save()

    def init(self):
        self._update_from_external()

    def is_name_blacklisted(self, user_name, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            for i in self.twitch_names:
                if i == user_name:
                    return True
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False

    def is_id_blacklisted(self, user_id, user_id_type: UserIDType):
        if user_id_type == UserIDType.TWITCH:
            for i in self.twitch_ids:
                if i == user_id:
                    return True
        if user_id_type == UserIDType.YOUTUBE:
            pass
        return False

    def _update_from_external(self):
        tm = TimeMeasure()
        bots = blacklist_crawler.get_twitch_bot_names()
        for bot_name in bots["names"]:
            if not self.is_name_blacklisted(bot_name, UserIDType.TWITCH):
                self.twitch_names.append(bot_name)
        for bot_id in bots["ids"]:
            if not self.is_id_blacklisted(bot_id, UserIDType.TWITCH):
                self.twitch_ids.append(bot_id)
        self._save()
        self._clear_blacklisted_character_files()
        end = tm.end()
        logger.log(logger.DEV, "Parsing external Blacklist took: " + end + "s")

    def _clear_blacklisted_character_files(self):
        for name in self.twitch_names:
            self.hurby.char_manager.delete_character(name, UserIDType.TWITCH)

    def _save(self):
        blacklist_dict = {
            "twitch_names": self.twitch_names,
            "twitch_ids": self.twitch_ids,
            "youtube_ids": self.youtube_ids,
            "mails": self.mails
        }
        json_loader.save_json(Blacklist.BLACKLIST_FILE, blacklist_dict)
