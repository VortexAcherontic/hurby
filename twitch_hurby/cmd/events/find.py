import random

from character.character import Character
from utils import hurby_utils


class EventFind:
    def __init__(self, json_data, hurby):
        self.hurby = hurby
        self.trigger = json_data["trigger"]
        self.find_credits = json_data["find_credits"]
        self.find_items = json_data["find_items"]
        self.credit_find_min = json_data["credit_find_min"]
        self.credit_find_max = json_data["credit_find_max"]
        self.event_end = json_data["event_end"]
        self.loot_credits = json_data["loot_credits"]
        self.loot_items = json_data["loot_items"]

    def issue_event(self):
        all_chars = self.hurby.char_manager.chars
        lucky_one: Character = all_chars[random.randint(0, len(all_chars) - 1)]
        while lucky_one is None:
            lucky_one: Character = all_chars[random.randint(0, len(all_chars) - 1)]
        if (random.random() > 0.5) & self.find_items:
            pass
        else:
            min_cred = self.credit_find_min
            max_cred = self.credit_find_max
            found_creds = random.randint(min_cred, max_cred)
            lucky_one.credits += found_creds
            lucky_one.save()

            msg = hurby_utils.get_random_reply(self.event_end)
            msg = msg.replace("$user", lucky_one.twitchid)
            cred_repl = hurby_utils.get_random_reply(self.loot_credits)
            cred_repl = cred_repl.replace("$amount", str(found_creds))
            msg = msg.replace("$loot", cred_repl)
            irc = self.hurby.twitch_receiver.twitch_listener
            irc.send_message(msg)
