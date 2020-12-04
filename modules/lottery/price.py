class LotteryPrice:
    def __init__(self, json_data):
        self.amount = json_data["amount"]
        self.title = json_data["title"]
        self.value = json_data["value"]
