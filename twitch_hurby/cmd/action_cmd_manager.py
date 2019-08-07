class ActionCMDManager:
    def __init__(self):
        self.actions = [None] * 10

    def call_action(self, cmd, parameters):
        for i in range(0, len(self.actions)):
            if cmd == self.actions[i]:
                self.actions[i].callAction(parameters)
                break

    def create_action(self, json):
        pass
