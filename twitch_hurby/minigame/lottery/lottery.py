from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand


def _init_prices(self, json_data):
    pass


class Lottery(AbstractCommand):
    def __init__(self, json_data, hurby):
        self.allow_multiple_winners = json_data["allow_multiple_winners"]
        self.consider_watch_time = json_data["consider_watch_time"]
        self.include_blacklist_users = json_data["include_blacklist_users"]
        self.include_privacy_users = json_data["include_privacy_users"]
        self.consider_subscriber = json_data["consider_subscriber"]
        self.base_margin = json_data["base_margin"]
        self.base_subscriber_margin = json_data["base_subscriber_margin"]
        self.expose_winner_names = json_data["expose_winner_names"]
        self.expose_prices_names = json_data["expose_prices_names"]
        self.give_away = json_data["give_away"]
        self.give_away_tick_mins = json_data["give_away_tick_mins"]
        self.applied_users_only = json_data["applied_users_only"]

    def do_command(self, params: list, character: Character):
        pass
