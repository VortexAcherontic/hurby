import random
from os import listdir
from os.path import isfile, join


def append_element_to_array(array: list, ele):
    tmp = array
    array = [None] * len(tmp) + 1
    for i in range(0, len(tmp)):
        array[i] = tmp[i]
    array[len(array) + 1] = ele
    return array


def get_random_reply(responses: list) -> str:
    return responses[random.randint(0, len(responses) - 1)]


def get_all_files_in_path(path: str):
    return [f for f in listdir(path) if isfile(join(path, f))]


def remove_doubles_from_list(my_list: list):
    return list(dict.fromkeys(my_list))
