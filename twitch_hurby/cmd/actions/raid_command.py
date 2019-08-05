import math
import random
import time

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger


class RaidCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = CMDResponseRealms(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        description = json_data["description"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm, description)
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
        self.participants: [Character] = None
        self.hurby = hurby
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
        self.overall_credits_spend = 0

    def do_command(self, params: list, character: Character):
        if self._input_valid(params) and character is not None:
            credit_spend = params[0]
            msg = ""
            irc = self.hurby.twitch_receiver.twitch_listener
            if self._invokable():
                if not self._participating(character):
                    if not self._insufficient_credits(character, int(credit_spend)):
                        character.credits -= int(credit_spend)
                        character.save()
                        if self.in_preparation:
                            self.participants.append(character)
                            self.credits_spend.append(credit_spend)
                            msg = self.reply_join[random.randint(0, len(self.reply_join) - 1)]
                        else:
                            msg = self.reply_start[random.randint(0, len(self.reply_join) - 1)]
                            self.participants = [character]
                            self.credits_spend = [credit_spend]
                            countdown_thread = RaidCountdownThread(self)
                            countdown_thread.start()
                        self.overall_credits_spend += int(credit_spend)
                        msg = msg.replace("$user_id", character.twitchid)
                        msg = msg.replace("$credits_spend", str(credit_spend))
                    else:
                        msg = self.insufficient_credits[random.randint(0, len(self.insufficient_credits) - 1)]
                        msg = msg.replace("$user_credits", str(character.credits))
                        logger.log(logger.INFO, msg)
                else:
                    msg = self.already_participating[random.randint(0, len(self.already_participating) - 1)]
            else:
                msg = self.raid_in_cooldown[random.randint(0, len(self.raid_in_cooldown) - 1)]
            irc.send_message(msg)

    def _input_valid(self, params: list):
        irc = self.hurby.twitch_receiver.twitch_listener
        msg = ""
        if len(params) < 1:
            msg = self.raid_error_no_credits[random.randint(0, len(self.raid_error_no_credits) - 1)]
            irc.send_message(msg)
            return False
        else:
            try:
                test = int(params[0])
                if test < 0:
                    return False
            except Exception:
                msg = self.raid_error_parse_credits[random.randint(0, len(self.raid_error_parse_credits) - 1)]
                irc.send_message(msg)
                return False
        return True

    def _insufficient_credits(self, char: Character, credits_spend: int):
        return char.credits < credits_spend

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


# This threads takes care about the preperation time and will invoke the RaidThread after it is finished
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
            logger.log(logger.INFO, "Raid in: " + str(self.countdown) + " Seconds")
            if self.countdown == 10:
                self.irc.send_message(self.response_10[random.randint(0, len(self.response_10) - 1)])
        self.root_cmd.in_preparation = False
        if len(self.root_cmd.participants) < self.root_cmd.min_participants:
            msg = self.root_cmd.insufficient_participants[
                random.randint(0, len(self.root_cmd.insufficient_participants) - 1)]
            msg.replace("$min_participants", str(self.root_cmd.min_participants))
            self.root_cmd.participants = None
            self.irc.send_message(msg)
        else:
            self.irc.send_message(self.raid_starting[random.randint(0, len(self.raid_starting) - 1)])
            raid_thread = RaidThread(self.root_cmd)
            raid_thread.run()


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
                char.credits += credits_won
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
        irc = self.root_cmd.hurby.twitch_receiver.twitch_listener
        logger.log(logger.INFO, "Raid is ready")
        msg = self.raid_ready[random.randint(0, len(self.raid_ready) - 1)]
        self.irc.send_message(msg)
        self.root_cmd.ready = True
