import errno
import os
from enum import Enum

from hurby.character.character import Character
from hurby.modules.lottery.lottery import Lottery
from hurby.utils import json_loader, hurby_utils
from hurby.utils.const import CONST
from hurby.utils.json_loader import load_json


class ParticipateStatus(Enum):
    SUCCESS = 0
    IS_FULL = 1
    INSUFFICIENT_CREDITS = 2
    MAX_TICKETS_REACHED = 3
    LOTTERY_INACTIVE = 4
    NO_ACTIVE_LOTTERY = 5
    NOT_ENOUGH_WATCH_TIME = 6


def _load_lotteries():
    lottery_files = hurby_utils.get_all_files_in_path(CONST.DIR_LOTTERIES_ABSOLUTE)
    lotteries = []
    current_id = 0
    for file in lottery_files:
        absolute_file = CONST.DIR_LOTTERIES_ABSOLUTE + "/" + file
        lottery_json = json_loader.load_json(absolute_file)
        lotteries.append(Lottery(lottery_json, absolute_file, current_id))
        current_id += 1
    return lotteries


def write_lottery_winner(lottery_name, price, winner_name):
    path = CONST.DIR_LOTTERIES_WINNERS_ABSOLUTE
    file = path + "/" + lottery_name + "_winners.txt"
    _mkdir_p_winners(path)
    with open(file, "a") as myfile:
        myfile.write(winner_name + ": " + price.price_title + " " + price.price_value + "\n")


def _mkdir_p_winners(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class LotteryManager:
    def __init__(self, hurby):
        json_data = load_json(CONST.DIR_LOTTERIES_BASE_ABSOLUTE + "/" + CONST.FILE_CONF_LOTTERY)
        self.hurby = hurby
        self.participation_requires_tickets = json_data["participation_requires_tickets"]
        self.max_tickets = json_data["max_tickets"]
        self.ticket_price = json_data["ticket_price"]
        self.expose_winner = json_data["expose_winner"]
        self.min_watch_time_in_mins = json_data["min_watch_time_in_mins"]
        self.always_allow_supporters = json_data["always_allow_supporters"]
        self.expose_won_price_title = json_data["expose_won_price_title"]
        self.only_draw_winner = json_data["only_draw_winner"]
        self.error_lottery_full_response = json_data["error_lottery_full_response"]
        self.error_insufficient_credits_response = json_data["error_insufficient_credits_response"]
        self.error_insufficient_watchtime_response = json_data["error_insufficient_watchtime_response"]
        self.error_max_tickets_reached = json_data["error_max_tickets_reached"]
        self.error_max_participants_reached = json_data["error_max_participants_reached"]
        self.success_participate = json_data["success_participate"]
        self.winner_drawn_response_no_expose = json_data["winner_drawn_response_no_expose"]
        self.winner_drawn_response_expose_winner = json_data["winner_drawn_response_expose_winner"]
        self.winner_drawn_response_expose_winner_and_price_title = json_data[
            "winner_drawn_response_expose_winner_and_price_title"]
        self.winner_drawn_response_expose_price_title = json_data["winner_drawn_response_expose_price_title"]
        self.error_lottery_is_inactive = json_data["error_lottery_is_inactive"]
        self.lottery_started_response = json_data["lottery_started_response"]
        self.response_applied_for_all = json_data["response_applied_for_all"]
        self.no_lotteries_response = json_data["no_lotteries_response"]
        self.running_lotteries_response_header = json_data["running_lotteries_response_header"]
        self.running_lotteries_response_item = json_data["running_lotteries_response_item"]
        self.lottery_ended_response = json_data["lottery_ended_response"]
        self.error_no_price_left = json_data["error_no_price_left"]
        self._lotteries = _load_lotteries()

    def try_participate(self, character: Character, lottery_id: int):
        if self.has_active_lotteries():
            lottery: Lottery = self._lotteries[lottery_id]
            if lottery.is_active():
                if not lottery.is_full():
                    if not self.participation_requires_tickets:
                        if self.min_watch_time_in_mins > 0:
                            if self._has_enough_watch_time(character) or character.is_supporter:
                                lottery.apply_for_lottery(character.uuid)
                                return ParticipateStatus.SUCCESS
                            else:
                                return ParticipateStatus.NOT_ENOUGH_WATCH_TIME
                        else :
                            lottery.apply_for_lottery(character.uuid)
                    elif character.get_credits() >= self.ticket_price or character.is_supporter:
                        tickets = lottery.get_tickets_for_user(character.uuid)
                        if tickets != self.max_tickets:
                            if character.is_supporter:
                                lottery.apply_for_lottery(character.uuid)
                            else:
                                character.remove_credits(self.ticket_price)
                                lottery.apply_for_lottery(character.uuid)
                            return ParticipateStatus.SUCCESS
                        else:
                            return ParticipateStatus.MAX_TICKETS_REACHED
                    else:
                        return ParticipateStatus.INSUFFICIENT_CREDITS
                else:
                    return ParticipateStatus.IS_FULL
            else:
                return ParticipateStatus.LOTTERY_INACTIVE
        else:
            return ParticipateStatus.NO_ACTIVE_LOTTERY

    def get_amount_of_lotteries(self):
        return len(self._lotteries)

    def get_amount_of_inactive_lotteries(self):
        inactive = 0
        for lot in self._lotteries:
            if not lot.is_active():
                inactive += 1
        return inactive

    def get_amount_of_active_lotteries(self):
        active = 0
        for lot in self._lotteries:
            if lot.is_active():
                active += 1
        return active

    def start_lottery(self, lottery_id):
        self._lotteries[lottery_id].start_lottery()

    def end_lottery(self, lottery_id):
        self._lotteries[lottery_id].end_lottery()

    def get_lottery_name(self, lottery_id):
        return self._lotteries[lottery_id].lottery_title

    def get_active_lottery_names(self):
        lottery_names = []
        for l in self._lotteries:
            if l.is_active():
                lottery_names.append(l.lottery_title)
        return lottery_names

    def get_active_lottery_descriptions(self):
        lottery_descriptions = []
        for l in self._lotteries:
            if l.is_active():
                lottery_descriptions.append(l.lottery_description)
        return lottery_descriptions

    def get_active_lottery_ids(self):
        lottery_ids = []
        current_id = 0
        while current_id < len(self._lotteries):
            current_lottery = self._lotteries[current_id]
            if current_lottery.is_active():
                lottery_ids.append(current_id)
            current_id += 1
        return lottery_ids

    def get_first_inactive_lottery(self):
        for lot in self._lotteries:
            if not lot.is_active():
                return lot
        return None

    def get_first_active_lottery(self):
        for lot in self._lotteries:
            if lot.is_active():
                return lot
        return None

    def get_lottery(self, lottery_id):
        return self._lotteries[lottery_id]

    def has_active_lotteries(self):
        for lot in self._lotteries:
            if lot.is_active():
                return True
        return False

    def _has_enough_watch_time(self, character: Character):
        return character.watchtime_min >= self.min_watch_time_in_mins
