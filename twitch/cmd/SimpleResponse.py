class SimpleResponse:
    def __init__(self, json):
        self.cmd = json["cmd"]
        self.type = json["type"]
        self.realm = json["realm"]
        self.reply = json["reply"]