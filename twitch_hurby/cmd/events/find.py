import random

from character.character import Character
from items.base_item import BaseItem
from utils import hurby_utils


def _value_of_items(items) -> int:
    summarize = 0
    for i in items:
        summarize += i.value
    return summarize


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
        if all_chars is not None:
            lucky_one: Character = all_chars[random.randint(0, len(all_chars) - 1)]
            min_value = self.credit_find_min
            max_value = self.credit_find_max
            found_value = random.randint(min_value, max_value)

            while lucky_one is None:
                lucky_one: Character = all_chars[random.randint(0, len(all_chars) - 1)]
            if (random.random() > 0.5) & self.find_items:
                items = [BaseItem]
                items_value = _value_of_items(items)
                while items_value > found_value:
                    rnd_item: BaseItem = self.hurby.item_manager.get_random_item
                    tmp_sum = items_value + rnd_item.value
                    if tmp_sum <= found_value:
                        items.append(rnd_item)
            else:
                lucky_one.credits += found_value
                lucky_one.save()
                msg = hurby_utils.get_random_reply(self.event_end)
                msg = msg.replace("$user", lucky_one.twitchid)
                cred_repl = hurby_utils.get_random_reply(self.loot_credits)
                cred_repl = cred_repl.replace("$amount", str(found_value))
                msg = msg.replace("$loot", cred_repl)
                irc = self.hurby.twitch_receiver.twitch_listener
                irc.send_message(msg)
