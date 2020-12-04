from uuid import UUID

from modules.lottery.price import LotteryPrice
from utils import hurby_utils, json_loader


def _build_prices(prices_json):
    prices = []
    for p in prices_json:
        prices.append(LotteryPrice(p))
    return prices


class Lottery:
    def __init__(self, json_data, lottery_file_name: str):
        self.lottery_file_name = lottery_file_name
        self.participants_uuids = []
        self.lottery_title = json_data["lottery_title"]
        self.lottery_description = json_data["lottery_description"]
        self.max_participants = json_data["max_participants"]
        self.prices = _build_prices(json_data["prices"])

    def apply_for_lottery(self, character_uuid: UUID):
        if not self.is_full(self):
            self.participants_uuids.append(character_uuid)
            return True
        return False

    def is_full(self):
        if self.max_participants <= 0:
            return False
        else:
            return self.participants_uuids == self.max_participants - 1

    def draw_price(self):
        if self._is_price_left():
            price: LotteryPrice = self._random_price()
            while price.amount == 0:
                price = self._random_price()
            price.amount = price.amount - 1
            return price
        return None

    def draw_winner(self):
        return self.participants_uuids[hurby_utils.get_random_in_range(0, len(self.participants_uuids) - 1)]

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
        return False

    def _random_price(self):
        price_id = hurby_utils.get_random_in_range(0, len(self.prices))
        return self.prices[price_id]

    def _dump_lottery(self):
        json_loader.save_json(self.lottery_file_name, self._to_dict())

    def _to_dict(self):
        return {
            "lottery_title": self.lottery_title,
            "lottery_description": self.lottery_description,
            "max_participants": self.max_participants,
            "prices": [self._prices_to_array()]
        }

    def _prices_to_array(self):
        prices = []
        for p in self.prices:
            price_dict = {
                "price_title": p.title,
                "price_value": p.value,
                "amount": p.amount
            }
            prices.append(price_dict)
