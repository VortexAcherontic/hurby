class LotteryPrice:
    def __init__(self, json_data):
        self.amount = json_data["amount"]
        self.price_title = json_data["price_title"]
        self.price_value = json_data["price_value"]
        self.only_if_others_empty = json_data["only_if_others_empty"]
