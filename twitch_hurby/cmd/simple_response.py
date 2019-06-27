import random


class SimpleResponse:
    def __init__(self, json):
        self.cmd = json["cmd"]
        self.type = json["type"]
        self.reply = json["reply"]

    def get_cmd(self):
        return self.cmd

    def respond(self):
        if isinstance(self.reply, list):
            return self.reply[random.randint(0, len(self.reply) - 1)]
        else:
            return self.reply
