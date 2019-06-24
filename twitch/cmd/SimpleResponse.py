class SimpleResponse:
    def __init__(self, json):
        self.cmd = json["cmd"]
        self.type = json["type"]
        self.realm = json["realm"]
        self.reply = json["reply"]

    def get_cmd(self):
        return self.cmd

    def respond(self):
        return self.reply