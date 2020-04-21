class Price:

    def __init__(self, json_data):
        self.name = json_data["name"]
        self.amount = json_data["amount"]
        self.value = json_data["value"]