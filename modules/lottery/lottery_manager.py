from enum import Enum

from character.character import Character
from hurby import Hurby
from modules.lottery.lottery import Lottery
from utils.const import CONST
from utils.json_loader import load_json


class ParticipateStatus(Enum):
    SUCCESS = 0
    IS_FULL = 1
    INSUFFICIENT_CREDITS = 2
    MAX_TICKETS_REACHED = 3


def _load_lotteries():
    return []


class LotteryManager:
    def __init__(self, hurby: Hurby):
        json_data = load_json(CONST.DIR_LOTTERIES_BASE_ABSOLUTE + "/" + CONST.FILE_CONF_LOTTERY)
        self.hurby = hurby
        self.participation_requires_tickets = json_data["participation_requires_tickets"]
        self.max_tickets = json_data["max_tickets"]
        self.ticket_price = json_data["ticket_price"]
        self.expose_winner = json_data["expose_winner"]
        self.expose_won_price_title = json_data["expose_won_price_title"]
        self.error_lottery_full_response = json_data["error_lottery_full_response"]
        self.error_insufficient_credits_response = json_data["error_insufficient_credits_response"]
        self.error_max_tickets_reached = json_data["error_max_tickets_reached"]
        self.error_max_participants_reached = json_data["error_max_participants_reached"]
        self.success_participate = json_data["success_participate"]
        self.winner_drawn_response_no_expose = json_data["winner_drawn_response_no_expose"]
        self.winner_drawn_response_expose_winner = json_data["winner_drawn_response_expose_winner"]
        self.winner_drawn_response_expose_winner_and_price_title = json_data[
            "winner_drawn_response_expose_winner_and_price_title"]
        self.winner_drawn_response_expose_price_title = json_data["winner_drawn_response_expose_price_title"]
        self.lotteries = _load_lotteries()

    def try_participate(self, character: Character, lottery_id: int):
        lottery: Lottery = self.lotteries[lottery_id]
        if not lottery.is_full():
            if not self.participation_requires_tickets:
                pass
            elif character.get_credits() >= self.ticket_price:
                tickets = lottery.get_tickets_for_user(character.uuid)
                if tickets != self.max_tickets:
                    character.remove_credits(self.ticket_price)
                    lottery.apply_for_lottery(character.uuid)
                    return ParticipateStatus.SUCCESS
                else:
                    return ParticipateStatus.MAX_TICKETS_REACHED
            else:
                return ParticipateStatus.INSUFFICIENT_CREDITS
        else:
            return ParticipateStatus.IS_FULL
