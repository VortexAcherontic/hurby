import random


def get_random_entry(array):
    # if array is list:
    return array[random.randint(0, len(array) - 1)]
    # elif array is str:
    #   return array
    # else:
    #   logger.log(logger.DEV, "No entry available")
