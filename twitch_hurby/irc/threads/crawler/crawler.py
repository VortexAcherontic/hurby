import time

import requests

from character.character import Character
from character.character_manager import CharacterManager
from character.user_id_types import UserIDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from twitch_hurby.helix import get_users, get_broadcaster_subscriptions
from twitch_hurby.irc.threads.crawler.chatter_types import ChatterType
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger
from utils.const import CONST


def _get_chatters_by_type(json_data, chatter_type: str):
    return json_data["chatters"][chatter_type]


class Crawler(HurbyThread):
    def __init__(self, twitch_config: TwitchConfig, char_manager: CharacterManager):
        HurbyThread.__init__(self)
        self.twitch_conf = twitch_config
        self.char_man = char_manager
        self.tick = twitch_config.crawler_time
        self.spend_time = twitch_config.spend_time
        self.crawl_cache = None
        self.credit_increase_base = twitch_config.credit_increase_base
        self.credit_increase_supporter = twitch_config.credit_increase_supporter

    def run(self):
        credit_thread = CreditSpendThread(self)
        credit_thread.start()
        logger.log(logger.INFO, "Running Twitch Crawler")
        while CONST.RUNNING:
            self._crawl_chatters(True)
            self._crawl_subscribers()
            time.sleep(self.tick * 60)
        logger.log(logger.INFO, "Stopped Twitch Crawler")

    def _crawl_chatters(self, force_re_fetch: bool):
        logger.log(logger.INFO, "Crawling chatters ... Force fetch: " + str(force_re_fetch))
        streamer = self.twitch_conf.streamer
        url = "https://tmi.twitch.tv/group/user/" + streamer + "/chatters"
        if force_re_fetch:
            r = requests.get(url)
            self.crawl_cache = r.json()

        mods = _get_chatters_by_type(self.crawl_cache, ChatterType.MODERATOR.value)
        broadcaster = _get_chatters_by_type(self.crawl_cache, ChatterType.BROADCASTER.value)
        admins = _get_chatters_by_type(self.crawl_cache, ChatterType.ADMINS.value)
        global_mods = _get_chatters_by_type(self.crawl_cache, ChatterType.GLOBAL_MODERATORS.value)
        staff = _get_chatters_by_type(self.crawl_cache, ChatterType.STAFF.value)
        viewer = _get_chatters_by_type(self.crawl_cache, ChatterType.VIEWER.value)
        vips = _get_chatters_by_type(self.crawl_cache, ChatterType.VIP.value)
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
        self.char_man.unload_offline_characters(all_chatters, UserIDType.TWITCH)

    def _init_character(self, name: str, chatter_type: ChatterType):
        try:
            if chatter_type == ChatterType.MODERATOR:
                self.char_man.get_character(name, UserIDType.TWITCH, PermissionLevels.MODERATOR, True, False)
            elif chatter_type == ChatterType.BROADCASTER:
                self.char_man.get_character(name, UserIDType.TWITCH, PermissionLevels.ADMINISTRATOR, True, False)
            else:
                self.char_man.get_character(name, UserIDType.TWITCH, PermissionLevels.EVERYBODY, True, False)
        except AttributeError as e:
            print(e)

    def _is_subscriber(self, user_id):
        pass

    def _crawl_subscribers(self):
        streamer = self.twitch_conf.streamer
        bearer_token = self.twitch_conf.access_token
        users_json = get_users.get_users_by_user_name([streamer], bearer_token)
        streamer_id = users_json["data"][0]["id"]
        subscribers = get_broadcaster_subscriptions.get_subscriptions(streamer_id, bearer_token)
        for sub in subscribers["data"]:
            tmpchar: Character = self.char_man.get_character(sub["user_name"].lower(), UserIDType.TWITCH)
            tmpchar.is_supporter = True
            tmpchar.save()

    def _resolve_channel_id(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.twitch_conf.client_id,
            'Authorization': 'OAuth ' + self.twitch_conf.oauth_token.split(":")[1],
        }
        response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
        return response.json()["_id"]


class CreditSpendThread(HurbyThread):
    def __init__(self, crawler: Crawler):
        HurbyThread.__init__(self)
        self.crawler = crawler
        self.spend_time = self.crawler.spend_time

    def run(self):
        logger.log(logger.INFO, "Running spend Thread...")
        while CONST.RUNNING:
            time.sleep(self.spend_time * 60)
            logger.log(logger.INFO, "Spending credits ...")
            if self.crawler.char_man.chars is not None:
                for c in self.crawler.char_man.chars:
                    if c.is_supporter:
                        c.credits += self.crawler.credit_increase_supporter
                    else:
                        c.credits += self.crawler.credit_increase_base
                    c.save()
            else:
                logger.log(logger.INFO, "No Chars :/")
