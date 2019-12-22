import random
import time

from character.character import Character
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import hurby_utils


class EventRob:
    def __init__(self, json_data, hurby):
        self.hurby = hurby
        self.trigger = json_data["trigger"]
        self.steal_credits = json_data["steal_credits"]
        self.stealt_items = json_data["stealt_items"]
        self.credit_steal_min = json_data["credit_steal_min"]
        self.credit_steal_max = json_data["credit_steal_max"]
        self.event_duration_sec = json_data["event_duration_sec"]
        self.event_start = json_data["event_start"]
        self.event_end = json_data["event_end"]
        self.loot_credits = json_data["loot_credits"]
        self.loot_items = json_data["loot_items"]

    def issue_event(self):
        msg = hurby_utils.get_random_reply(self.event_start)
        irc = self.hurby.twitch_receiver.twitch_listener
        irc.send_message(msg)
        rob_thread = RobThread(self)
        rob_thread.start()
        rob_thread.join()


class RobThread(HurbyThread):
    def __init__(self, root_event: EventRob):
        HurbyThread.__init__(self)
        self.root_event = root_event
        self.countdown = root_event.event_duration_sec

    def run(self):
        time.sleep(self.countdown)
        all_chars = self.root_event.hurby.char_manager.chars
        if all_chars is not None and len(all_chars) > 0:
            victim: Character = all_chars[random.randint(0, len(all_chars) - 1)]
            if victim is not None:
                if (random.random() > 0.5) & self.root_event.stealt_items:
                    pass
                else:
                    min_cred = self.root_event.credit_steal_min
                    max_cred = self.root_event.credit_steal_max
                    stolen_creds = random.randint(min_cred, max_cred)
                    if victim.credits >= stolen_creds:
                        victim.credits -= stolen_creds
                    else:
                        stolen_creds = victim.credits
                        victim.credits = 0
                    victim.save()
                    msg = hurby_utils.get_random_reply(self.root_event.event_end)
                    msg = msg.replace("$victim", victim.twitchid)
                    cred_repl = hurby_utils.get_random_reply(self.root_event.loot_credits)
                    cred_repl = cred_repl.replace("$amount", str(stolen_creds))
                    msg = msg.replace("$loot", cred_repl)
                    irc = self.root_event.hurby.twitch_receiver.twitch_listener
                    irc.send_message(msg)
