import json
import urllib

from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import logger


class SearchCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = CMDResponseRealms(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm)
        self.hurby = hurby

    def do_command(self, params: list):
        search_string = params[0]
        logger.log(logger.INFO, "Searching for "+seartch_string)
        url = "https://api.duckduckgo.com/?q="+seartch_string+"&format=json&atb=v105-1"
        r = urllib.request.urlopen(url)
        string_data = r.read().decode('utf-8')
        json_data = json.loads(string_data)
        irc = self.hurby.twitch_receiver.twitch_listener
        logger.log(logger.INFO, "Result: "+json_data["AbstractText"])
        irc.send_message(json_data["AbstractText"])