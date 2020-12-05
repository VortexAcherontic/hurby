class LotteryPrice:
    def __init__(self, json_data):
        self.amount = json_data["amount"]
        self.title = json_data["price_title"]
        self.value = json_data["price_value"]
