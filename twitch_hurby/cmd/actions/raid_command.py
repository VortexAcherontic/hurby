import math
import random
import time

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger, hurby_utils


def _insufficient_credits(char: Character, credits_spend: int):
    return char.get_credits() < credits_spend


class RaidCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.cooldown = json_data["cooldown_min"]
        self.countdown = json_data["countdown_min"]
        self.in_preparation = False
        self.running = False
        self.ready = True
        self.duration = json_data["duration_min"]
        self.reply_start = json_data["reply_start"]
        self.reply_join = json_data["reply_join"]
        self.reply_success = json_data["reply_success"]
        self.reply_fail = json_data["reply_fail"]
        self.raid_ready = json_data["raid_ready"]
        self.min_credits = json_data["min_credits"]
        self.participants: [Character] = None
        self.credits_spend = None
        self.response_10_sec = json_data["response_10_sec"]
        self.insufficient_credits = json_data["insufficient_credits"]
        self.already_participating = json_data["already_participating"]
        self.raid_starting = json_data["raid_starting"]
        self.raid_error_no_credits = json_data["raid_error_no_credits"]
        self.raid_error_parse_credits = json_data["raid_error_parse_credits"]
        self.raid_in_cooldown = json_data["raid_in_cooldown"]
        self.win_ratio_base = json_data["win_ratio_base"]
        self.win_ratio_supporter = json_data["win_ratio_supporter"]
        self.win_template = json_data["win_template"]
        self.min_participants = json_data["min_participants"]
        self.insufficient_participants = json_data["insufficient_participants"]
        self.insufficient_credits_spend = json_data["insufficient_credits_spend"]
        self.overall_credits_spend = 0

    def do_command(self, params: list, character: Character):
        if self._input_valid(params) and character is not None:
            credit_spend = params[0]
            msg = ""
            if self._invokable():
                if not self._participating(character):
                    if not _insufficient_credits(character, int(credit_spend)):
                        if self._spend_min_credits(credit_spend):
                            character.remove_credits(int(credit_spend))
                            if self.in_preparation:
                                self.participants.append(character)
                                self.credits_spend.append(credit_spend)
                                msg = hurby_utils.get_random_reply(self.reply_join)
                            else:
                                msg = hurby_utils.get_random_reply(self.reply_join)
                                self.participants = [character]
                                self.credits_spend = [credit_spend]
                                countdown_thread = RaidCountdownThread(self)
                                countdown_thread.start()
                            self.overall_credits_spend += int(credit_spend)
                            msg = msg.replace("$user_id", character.twitchid)
                            msg = msg.replace("$credits_spend", str(credit_spend))
                        else:
                            msg = hurby_utils.get_random_reply(self.insufficient_credits_spend)
                            msg = msg.replace("$user_credits", str(character.get_credits))
                            msg = msg.replace("$min_credits", str(self.min_credits))
                            msg = msg.replace("$user_id", character.twitchid)
                    else:
                        msg = hurby_utils.get_random_reply(self.insufficient_credits_spend)
                        msg = msg.replace("$user_credits", str(character.get_credits))
                        msg = msg.replace("$min_credits", str(self.min_credits))
                        msg = msg.replace("$user_id", character.twitchid)
                        logger.log(logger.INFO, msg)
                else:
                    msg = hurby_utils.get_random_reply(self.already_participating)
            else:
                msg = hurby_utils.get_random_reply(self.raid_in_cooldown)
            self.irc.send_message(msg)

    def _spend_min_credits(self, credits_spend) -> bool:
        return int(credits_spend) >= self.min_credits

    def _input_valid(self, params: list):
        msg = ""
        if len(params) < 1:
            msg = hurby_utils.get_random_reply(self.raid_error_no_credits)
            self.irc.send_message(msg)
            return False
        else:
            try:
                test = int(params[0])
                if test < 0:
                    return False
            except ValueError:
                msg = hurby_utils.get_random_reply(self.raid_error_parse_credits)
                self.irc.send_message(msg)
                return False
        return True

    def _participating(self, char: Character):
        if self.participants is not None:
            for c in self.participants:
                if c.twitchid == char.twitchid:
                    return True
        return False

    def _invokable(self):
        if self.running:
            return False
        elif not self.ready:
            return False
        else:
            return True


# This threads takes care about the preparation time and will invoke the RaidThread after it is finished
class RaidCountdownThread(HurbyThread):
    def __init__(self, root_cmd: RaidCommand):
        HurbyThread.__init__(self)
        self.root_cmd = root_cmd
        self.countdown = root_cmd.countdown * 60
        self.response_10 = root_cmd.response_10_sec
        self.raid_starting = root_cmd.raid_starting
        self.irc = root_cmd.hurby.twitch_receiver.twitch_listener

    def run(self):
        logger.log(logger.INFO, "Starting Raid in: " + str(self.countdown) + " Seconds")
        self.root_cmd.in_preparation = True
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1
            logger.log(logger.DEV, "Raid in: " + str(self.countdown) + " Seconds")
            if self.countdown == 10:
                self.irc.send_message(hurby_utils.get_random_reply(self.response_10))
        self.root_cmd.in_preparation = False
        if len(self.root_cmd.participants) < self.root_cmd.min_participants:
            msg = self.root_cmd.insufficient_participants[
                random.randint(0, len(self.root_cmd.insufficient_participants) - 1)]
            msg.replace("$min_participants", str(self.root_cmd.min_participants))
            self._restore_spend_cookies()
            self.root_cmd.participants = None
            self.irc.send_message(msg)
        else:
            self.irc.send_message(self.raid_starting[random.randint(0, len(self.raid_starting) - 1)])
            raid_thread = RaidThread(self.root_cmd)
            raid_thread.run()

    def _restore_spend_cookies(self):
        logger.log(logger.DEV, "RaidCountdownThread: Restoring spend credits")
        lonely_chars: list[Character] = self.root_cmd.participants
        lonely_credits = self.root_cmd.credits_spend
        for x in range(0, len(lonely_chars)):
            lonely_chars[x].add_credits(lonely_credits[x])
            lonely_chars[x].save()


class RaidThread(HurbyThread):
    def __init__(self, root_cmd):
        HurbyThread.__init__(self)
        self.root_cmd: RaidCommand = root_cmd
        self.duration = self.root_cmd.duration
        self.irc = self.root_cmd.hurby.twitch_receiver.twitch_listener
        self.reply_fail = self.root_cmd.reply_fail
        self.reply_success = self.root_cmd.reply_success

    def run(self):
        logger.log(logger.INFO, "This Raid will take " + str(self.duration) + " Minutes")
        self.root_cmd.running = True
        self.root_cmd.ready = False
        time.sleep(self.duration * 60)
        logger.log(logger.INFO, "Raid finished")
        self._finish_raid()
        self.root_cmd.running = False
        raid_cooldown = RaidCooldownThread(self.root_cmd)
        raid_cooldown.start()

    def _finish_raid(self):
        rewards = {}
        for i in range(0, len(self.root_cmd.participants)):
            char = self.root_cmd.participants[i]
            spend = int(self.root_cmd.credits_spend[i])
            won = False
            win_ratio = random.random()
            win_ratio_increase = (2 - 2 / math.log1p(self.root_cmd.overall_credits_spend)) / 10
            logger.log(logger.INFO, "Win ratio for: " + char.twitchid + " is: " + str(win_ratio))
            if char.is_supporter:
                if win_ratio <= self.root_cmd.win_ratio_supporter + win_ratio_increase:
                    won = True
            else:
                if win_ratio <= self.root_cmd.win_ratio_base + win_ratio_increase:
                    won = True
            if won:
                credits_won = math.ceil(spend + spend * 0.5)
                char.add_credits(credits_won)
                rewards[char.twitchid] = credits_won
                char.save()
        if not bool(rewards):
            self.irc.send_message(self.reply_fail[random.randint(0, len(self.reply_fail) - 1)])
        else:
            winners_str = ""
            win_template = self.root_cmd.win_template[random.randint(0, len(self.root_cmd.win_template) - 1)]
            for key in rewards:
                tmp = win_template.replace("$user_id", key)
                tmp = tmp.replace("$reward", str(rewards[key]))
                winners_str += tmp + " | "
            msg = self.reply_success[random.randint(0, len(self.reply_success) - 1)]
            msg = msg.replace("$raid_results", winners_str)
            self.irc.send_message(msg)


class RaidCooldownThread(HurbyThread):
    def __init__(self, root_cmd: RaidCommand):
        HurbyThread.__init__(self)
        self.root_cmd = root_cmd
        self.cooldown = self.root_cmd.cooldown
        self.raid_ready = self.root_cmd.raid_ready
        self.irc = root_cmd.hurby.twitch_receiver.twitch_listener

    def run(self):
        logger.log(logger.INFO, "Raid will cool down for " + str(self.cooldown) + " Minutes")
        self.root_cmd.participants = None
        self.root_cmd.credits_spend = None
        time.sleep(self.cooldown * 60)
        logger.log(logger.INFO, "Raid is ready")
        msg = self.raid_ready[random.randint(0, len(self.raid_ready) - 1)]
        self.irc.send_message(msg)
        self.root_cmd.ready = True
