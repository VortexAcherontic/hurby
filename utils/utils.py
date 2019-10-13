import random


def get_random_entry(array):
    return array[random.randint(0, len(array) - 1)]
