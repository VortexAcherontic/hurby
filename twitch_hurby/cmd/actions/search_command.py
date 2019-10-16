import json
import urllib

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import logger


class SearchCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)

    def do_command(self, params: list, character: Character):
        search_string = params[0]
        logger.log(logger.INFO, "Searching for " + search_string)
        url = "https://api.duckduckgo.com/?q=" + search_string + "&format=json&atb=v105-1"
        r = urllib.request.urlopen(url)
        string_data = r.read().decode('utf-8')
        json_data = json.loads(string_data)
        logger.log(logger.INFO, "Result: " + json_data["AbstractText"])
        self.irc.send_message(json_data["AbstractText"])
