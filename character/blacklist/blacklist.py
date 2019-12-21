from character.blacklist.blacklist_updater import BlacklistUpdater
from character.user_id_types import UserIDType
from utils import json_loader, logger
from utils.const import CONST


class Blacklist:
    DIR_CHARACTER = CONST.DIR_APP_DATA_ABSOLUTE + "/characters"
    BLACKLIST_FILE = DIR_CHARACTER + "/" + CONST.FILE_BLACKLIST

    def __init__(self, hurby):
        self.blacklist_updater = BlacklistUpdater(self)
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
            self.save()

    def init(self):
        logger.log(logger.DEV, "Start BlacklistUpdater Thread")
        self.blacklist_updater.start()
        logger.log(logger.DEV, "Started BlacklistUpdater Thread, now running...")

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

    def clear_blacklisted_character_files(self):
        for name in self.twitch_names:
            self.hurby.char_manager.delete_character(name, UserIDType.TWITCH)

    def save(self):
        blacklist_dict = {
            "twitch_names": self.twitch_names,
            "twitch_ids": self.twitch_ids,
            "youtube_ids": self.youtube_ids,
            "mails": self.mails
        }
        json_loader.save_json(Blacklist.BLACKLIST_FILE, blacklist_dict)
