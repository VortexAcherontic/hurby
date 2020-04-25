class InsufficientCreditsException(Exception):
    def __init__(self, message, credits_left):
        super().__init__(message)
        self.credits_left = credits_left

