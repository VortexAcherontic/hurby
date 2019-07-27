import json
import time
import urllib.request

from character.character_manager import CharacterManager
from character.permission_levels import PermissionLevel
from character.user_id_types import UserIDType
from twitch_hurby.irc.threads.crawler.chatter_types import ChatterType
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger
from utils.const import CONST


class Crawler(HurbyThread):
    def __init__(self, twitch_config: TwitchConfig, char_manager: CharacterManager):
        HurbyThread.__init__(self)
        self.twitch_conf = twitch_config
        self.char_man = char_manager
        self.tick = twitch_config.crawler_time
        self.crawl_cache = None

    def run(self):
        logger.log(logger.INFO, "Running Twitch Crawler")
        while CONST.RUNNING:
            self.crawl_chatters(True)
            time.sleep(self.tick * 60)
        logger.log(logger.INFO, "Stopped Twitch Crawler")

    def crawl_chatters(self, force_re_fetch: bool):
        logger.log(logger.INFO, "Crawling chatters ...")
        streamer = self.twitch_conf.streamer
        url = "https://tmi.twitch.tv/group/user/" + streamer + "/chatters"
        if force_re_fetch:
            r = urllib.request.urlopen(url)
            string_data = r.read().decode('utf-8')
            self.crawl_cache = json.loads(string_data)

        mods = self._get_chatters_by_type(self.crawl_cache, ChatterType.MODERATOR.value)
        broadcaster = self._get_chatters_by_type(self.crawl_cache, ChatterType.BROADCASTER.value)
        admins = self._get_chatters_by_type(self.crawl_cache, ChatterType.ADMINS.value)
        global_mods = self._get_chatters_by_type(self.crawl_cache, ChatterType.GLOBAL_MODERATORS.value)
        staff = self._get_chatters_by_type(self.crawl_cache, ChatterType.STAFF.value)
        viewer = self._get_chatters_by_type(self.crawl_cache, ChatterType.VIEWER.value)
        vips = self._get_chatters_by_type(self.crawl_cache, ChatterType.VIP.value)
        all_chatters = mods + broadcaster + admins + global_mods + staff + viewer + vips
        for i in mods:
            self._init_character(i, ChatterType.MODERATOR)
        for i in broadcaster:
            self._init_character(i, ChatterType.BROADCASTER)
        for i in admins:
            self._init_character(i, ChatterType.ADMINS)
        for i in global_mods:
            self._init_character(i, ChatterType.GLOBAL_MODERATORS)
        for i in staff:
            self._init_character(i, ChatterType.STAFF)
        for i in viewer:
            self._init_character(i, ChatterType.VIEWER)
        for i in vips:
            self._init_character(i, ChatterType.VIP)
        self.char_man.unload_offline_character(all_chatters, UserIDType.TWITCH)

    def _get_chatters_by_type(self, json_data, chatter_type: str):
        return json_data["chatters"][chatter_type]

    def _init_character(self, name: str, chatter_type: ChatterType):
        known: bool = self.char_man.check_viewer_id(UserIDType.TWITCH, name)
        logger.log(logger.INFO, "Chatter: " + name + " is known: " + str(known))
        if not known:
            if chatter_type == ChatterType.MODERATOR:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.MODERATOR)
            elif chatter_type == ChatterType.BROADCASTER:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.ADMINISTRATOR)
            else:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.EVERY_BODY)
        else:
            self.char_man.load_character(user_id=name, id_type=UserIDType.TWITCH)

    def _is_subscriber(self, user_id):
        pass
