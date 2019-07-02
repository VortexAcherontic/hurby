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

    def run(self):
        logger.log(logger.INFO, "Running Twitch Crawler")
        while CONST.RUNNING:
            self._crawl_chatters()
            time.sleep(self.tick * 60)
        logger.log(logger.INFO, "Stopped Twitch Crawler")

    def _crawl_chatters(self):
        streamer = self.twitch_conf.streamer
        url = "https://tmi.twitch.tv/group/user/" + streamer + "/chatters"
        r = urllib.request.urlopen(url)
        string_data = r.read().decode('utf-8')
        json_data = json.loads(string_data)
        mods = self._get_chatters_by_type(json_data, ChatterType.MODERATOR.value)
        broadcaster = self._get_chatters_by_type(json_data, ChatterType.BROADCASTER.value)
        admins = self._get_chatters_by_type(json_data, ChatterType.ADMINS.value)
        global_mods = self._get_chatters_by_type(json_data, ChatterType.GLOBAL_MODERATORS.value)
        staff = self._get_chatters_by_type(json_data, ChatterType.STAFF.value)
        viewer = self._get_chatters_by_type(json_data, ChatterType.VIEWER.value)
        vips = self._get_chatters_by_type(json_data, ChatterType.VIP.value)
        for i in mods:
            self._check_and_create_character(i, ChatterType.MODERATOR)
        for i in broadcaster:
            self._check_and_create_character(i, ChatterType.BROADCASTER)
        for i in admins:
            self._check_and_create_character(i, ChatterType.ADMINS)
        for i in global_mods:
            self._check_and_create_character(i, ChatterType.GLOBAL_MODERATORS)
        for i in staff:
            self._check_and_create_character(i, ChatterType.STAFF)
        for i in viewer:
            self._check_and_create_character(i, ChatterType.VIEWER)
        for i in vips:
            self._check_and_create_character(i, ChatterType.VIP)

    def _get_chatters_by_type(self, json_data, chatter_type: str):
        return json_data["chatters"][chatter_type]

    def _check_and_create_character(self, name: str, chatter_type: ChatterType):
        known = self.char_man.check_viewer_id(UserIDType.TWITCH, name)
        if not known:
            if chatter_type == ChatterType.MODERATOR:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.MODERATOR)
            elif chatter_type == ChatterType.BROADCASTER:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.ADMINISTRATOR)
            else:
                self.char_man.create_new_character(UserIDType.TWITCH, name, PermissionLevel.EVERY_BODY)

        logger.log(logger.INFO, "Chatter: " + name + " is known: " + str(known))
