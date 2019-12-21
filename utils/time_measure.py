import time


class TimeMeasure:
    def __init__(self):
        self.start = time.time()

    def end(self):
        return time.time() - self.start
