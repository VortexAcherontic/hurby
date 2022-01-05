import time

import requests

from character.character import Character
from character.character_manager import CharacterManager
from character.user_id_types import UserIDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from twitch_hurby.helix import get_users, get_broadcaster_subscriptions
from twitch_hurby.irc.threads.crawler import UpdateWatchTimeThread, CreditSpendThread
from twitch_hurby.irc.threads.crawler.chatter_types import ChatterType
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from twitch_hurby.tmi.get_chatters import get_chatters_for_channels
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger
from utils.const import CONST


class Crawler(HurbyThread):
    def __init__(self, twitch_config: TwitchConfig, char_manager: CharacterManager):
        HurbyThread.__init__(self)
        self.twitch_conf = twitch_config
        self.char_man = char_manager
        self.tick = twitch_config.crawler_time
        self.spend_time = twitch_config.spend_time
        self.credit_increase_base = twitch_config.credit_increase_base
        self.credit_increase_supporter = twitch_config.credit_increase_supporter

    def run(self):
        credit_thread = CreditSpendThread.CreditSpendThread(self, self.twitch_conf)
        credit_thread.start()
        watchtime_thread = UpdateWatchTimeThread.UpdateWatchTimeThread(self, self.twitch_conf)
        watchtime_thread.start()
        logger.log(logger.INFO, "Running Twitch Crawler")
        while CONST.RUNNING:
            self._crawl_chatters(True)
            self._crawl_subscribers()
            time.sleep(self.tick * 60)
        logger.log(logger.INFO, "Stopped Twitch Crawler")

    def _crawl_chatters(self, force_re_fetch: bool):
        logger.log(logger.INFO, "Crawling chatters ... Force fetch: " + str(force_re_fetch))
        chatters_dict = get_chatters_for_channels(self.twitch_conf.channel_names)

        mods = chatters_dict[ChatterType.MODERATOR]
        broadcaster = chatters_dict[ChatterType.BROADCASTER]
        admins = chatters_dict[ChatterType.ADMINS]
        global_mods = chatters_dict[ChatterType.GLOBAL_MODERATORS]
        staff = chatters_dict[ChatterType.STAFF]
        viewer = chatters_dict[ChatterType.VIEWER]
        vips = chatters_dict[ChatterType.VIP]
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
        self.char_man.unload_offline_characters(self.twitch_conf.channel_names, UserIDType.TWITCH)

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
        users_json = get_users.get_users_by_user_name([streamer], self.twitch_conf)
        streamer_id = users_json["data"][0]["id"]
        subscribers = get_broadcaster_subscriptions.get_subscriptions(streamer_id, self.twitch_conf)
        for sub in subscribers["data"]:
            tmpchar: Character = self.char_man.get_character(sub["user_name"].lower(), UserIDType.TWITCH)
            if tmpchar is not None:
                tmpchar.is_supporter = True
                tmpchar.save()
                self.char_man.unload_offline_characters(self.twitch_conf.channel_names, UserIDType.TWITCH)

    def _resolve_channel_id(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.twitch_conf.client_id,
            'Authorization': 'OAuth ' + self.twitch_conf.oauth_token.split(":")[1],
        }
        response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
        return response.json()["_id"]
