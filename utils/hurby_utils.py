import random


def append_element_to_array(array: list, ele):
    tmp = array
    array = [None] * len(tmp) + 1
    for i in range(0, len(tmp)):
        array[i] = tmp[i]
    array[len(array) + 1] = ele
    return array


def get_random_reply(responses: list) -> str:
    return responses[random.randint(0, len(responses) - 1)]
