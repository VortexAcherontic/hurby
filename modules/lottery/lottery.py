from uuid import UUID

from modules.lottery.price import LotteryPrice
from utils import hurby_utils, json_loader


def _build_prices(prices_json):
    prices = []
    for p in prices_json:
        prices.append(LotteryPrice(p))
    return prices


class Lottery:
    def __init__(self, json_data, lottery_file_name: str, internal_id: int):
        self.lottery_id = internal_id
        self.lottery_file_name = lottery_file_name
        self.participants_uuids = []
        self.lottery_title = json_data["lottery_title"]
        self.lottery_description = json_data["lottery_description"]
        self.max_participants = json_data["max_participants"]
        self.subscribers_only = json_data["subscribers_only"]
        self.followers_only = json_data["followers_only"]
        self.consider_watch_time = json_data["consider_watch_time"]
        self.consider_subscriber = json_data["consider_subscriber"]
        self.consider_follower = json_data["consider_follower"]
        self.extra_tickets_follower = json_data["extra_tickets_follower"]
        self.extra_tickets_subscriber = json_data["extra_tickets_subscriber"]
        self.extra_tickets_watch_time = json_data["extra_tickets_watch_time"]
        self.watch_time_in_mins_for_extra_tickets = json_data["watch_time_in_mins_for_extra_tickets"]
        self.prices = _build_prices(json_data["prices"])
        self._is_running = False

    def start_lottery(self):
        self._is_running = True

    def end_lottery(self):
        self._is_running = False

    def is_active(self):
        return self._is_running

    def apply_for_lottery(self, character_uuid: UUID):
        if not self.is_full():
            self.participants_uuids.append(character_uuid)
            return True
        return False

    def is_full(self):
        if self.max_participants <= 0:
            return False
        else:
            return self.participants_uuids == self.max_participants - 1

    def has_prices(self):
        return self._is_price_left()

    def draw_price(self):
        if self.is_active():
            if self._is_price_left():
                price: LotteryPrice = self._random_price()
                while price.amount == 0:
                    price = self._random_price()
                if price.amount != -1:
                    price.amount = price.amount - 1
                self._dump_lottery()
                return price
            return None
        else:
            return None

    def draw_winner(self):
        if self.is_active():
            return self.participants_uuids[hurby_utils.get_random_in_range(0, len(self.participants_uuids) - 1)]
        else:
            return None

    def get_tickets_for_user(self, user_uuid: UUID):
        count = 0
        if self.participants_uuids.__contains__(user_uuid):
            for id in self.participants_uuids:
                if id == user_uuid:
                    count += 1
        return count

    def _is_price_left(self):
        for p in self.prices:
            if p.amount > 0:
                return True
            elif p.amount == -1:
                return True
        return False

    def _random_price(self):
        price_id = hurby_utils.get_random_in_range(0, len(self.prices)-1)
        return self.prices[price_id]

    def _dump_lottery(self):
        json_loader.save_json(self.lottery_file_name, self._to_dict())

    def _to_dict(self):
        return {
            "lottery_title": self.lottery_title,
            "lottery_description": self.lottery_description,
            "max_participants": self.max_participants,
            "subscribers_only": self.subscribers_only,
            "followers_only": self.followers_only,
            "consider_watch_time": self.consider_watch_time,
            "consider_subscriber": self.consider_subscriber,
            "consider_follower": self.consider_follower,
            "extra_tickets_follower": self.extra_tickets_follower,
            "extra_tickets_subscriber": self.extra_tickets_subscriber,
            "extra_tickets_watch_time": self.extra_tickets_watch_time,
            "watch_time_in_mins_for_extra_tickets": self.watch_time_in_mins_for_extra_tickets,
            "prices": self._prices_to_array()
        }

    def _prices_to_array(self):
        prices = []
        for p in self.prices:
            price_dict = {
                "price_title": p.price_title,
                "price_value": p.price_value,
                "only_if_others_empty": p.only_if_others_empty,
                "amount": p.amount
            }
            prices.append(price_dict)
        return prices
