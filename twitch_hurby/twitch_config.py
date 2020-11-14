from config.bot_config import BotConfig
from twitch_hurby.cmd import cmd_loader, event_loader
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.event_thread import EventThread
from twitch_hurby.helix.get_bearer_token import get_bearer_access_token
from twitch_hurby.helix.twitch_scopes import TwitchScopes
from utils import logger, json_loader, hurby_utils
from utils.const import CONST


class TwitchConfig:
    CMD_PATH = CONST.DIR_APP_DATA_ABSOLUTE + "/templates/commands/twitch/"
    EVENT_PATH = CONST.DIR_APP_DATA_ABSOLUTE + "/templates/events/twitch/"
    CONFIG_FILE = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_CONF_TWITCH
    HOST = "irc.twitch.tv"
    PORT = 6667

    def __init__(self, hurby):
        self.hurby = hurby

        twitch_json = json_loader.load_json(TwitchConfig.CONFIG_FILE)
        self.onlyfiles = hurby_utils.get_all_files_in_path(TwitchConfig.CMD_PATH)
        self.cmds = [AbstractCommand] * len(self.onlyfiles)
        self.oauth_token = twitch_json["oauth_token"]
        self.channel_names = twitch_json["channel_names"]
        self.authorization_code = twitch_json["authorization_code"]
        self.streamer = twitch_json["streamer"]
        self.client_id = twitch_json["client_id"]
        self.client_secret = twitch_json["client_secret"]
        self.redirect_url = twitch_json["redirect_url"]
        self.enable_cron_jobs = twitch_json["enable_cron_jobs"]
        self.cron_job_time = twitch_json["cron_job_time"]
        self.cron_jobs = twitch_json["cron_jobs"]
        self.crawler_time = twitch_json["crawler_time_mins"]
        self.credit_increase_base = twitch_json["credit_increase_base"]
        self.credit_increase_supporter = twitch_json["credit_increase_supporter"]
        self.spend_time = twitch_json["spend_time"]
        self.bot_scopes = twitch_json["bot_scopes"]
        self.bot_username = self.hurby.get_bot_config().botname
        self.twitch_scopes = TwitchScopes()
        self.access_token = twitch_json["access_token"]
        self.expires_in = twitch_json["expires_in"]
        self.refresh_token = twitch_json["refresh_token"]

    def init(self):
        self._authorize()

    def load_cmds(self):
        self.cmds = [AbstractCommand] * 0
        for i in range(0, len(self.onlyfiles)):
            if self.onlyfiles[i].endswith(".json"):
                cmd_json = json_loader.load_json(TwitchConfig.CMD_PATH + self.onlyfiles[i])
                tmp_cmd = cmd_loader.create_cmd(cmd_json, self.hurby.get_bot_config(), self.hurby)
                if not _check_for_duplicate_trigger(self.cmds, tmp_cmd):
                    self.cmds.append(tmp_cmd)
        logger.log(logger.INFO, str(len(self.cmds)) + " commands loaded")

    def load_events(self):
        if self.hurby.get_bot_config().modules[BotConfig.MODULE_EVENTS]:
            onlyfiles_events = hurby_utils.get_all_files_in_path(TwitchConfig.EVENT_PATH)
            events = [None] * 0
            for i in range(0, len(onlyfiles_events)):
                if onlyfiles_events[i].endswith(".json"):
                    event_json = json_loader.load_json(TwitchConfig.EVENT_PATH + onlyfiles_events[i])
                    events.append(event_loader.create_event(event_json, self.hurby))
            event_thread = EventThread(self.hurby, events)
            event_thread.start()

    def get_cmds(self) -> list:
        return self.cmds

    def save(self):
        config_dict = {
            "oauth_token": self.oauth_token,
            "channel_names": self.channel_names,
            "streamer": self.streamer,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_url": self.redirect_url,
            "authorization_code": self.authorization_code,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "bot_scopes": self.bot_scopes,
            "enable_cron_jobs": self.enable_cron_jobs,
            "cron_job_time": self.cron_job_time,
            "cron_jobs": self.cron_jobs,
            "crawler_time_mins": self.crawler_time,
            "credit_increase_base": self.credit_increase_base,
            "credit_increase_supporter": self.credit_increase_supporter,
            "spend_time": self.spend_time
        }
        json_loader.save_json(TwitchConfig.CONFIG_FILE, config_dict)

    def _authorize(self):
        get_bearer_access_token(self)


def _check_for_duplicate_trigger(cmds, cmd: AbstractCommand) -> bool:
    if cmds is not None and cmd is not None:
        for c in cmds:
            if isinstance(cmd.trigger, list):
                for t in cmd.trigger:
                    if c.check_trigger(t):
                        _log_duplicate_trigger(t)
                        return True
            else:
                is_duplicate = c.check_trigger(cmd.trigger)
                if is_duplicate:
                    _log_duplicate_trigger(cmd.trigger)
                return is_duplicate
        return False


def _log_duplicate_trigger(trigger):
    logger.log(logger.WARN, "Duplicate trigger: " + trigger)
