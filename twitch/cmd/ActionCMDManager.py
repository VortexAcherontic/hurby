class ActionCMDManager:
    def __init__(self):
        self.actions = [None] * 10

    def callAction(self, cmd, parameters):
        for i in range(0, len(self.actions)):
            if cmd == self.actions[i]:
                self.actions[i].callAction(parameters)
                break

    def createAction(self, json):
        pass
