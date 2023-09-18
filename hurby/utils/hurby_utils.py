import random
from os import listdir
from os.path import isfile, join

from twitch.cmd.enums.permission_levels import PermissionLevels


def append_element_to_array(array: list, ele):
    tmp = array
    array = [None] * len(tmp) + 1
    for i in range(0, len(tmp)):
        array[i] = tmp[i]
    array[len(array) + 1] = ele
    return array


def get_random_reply(responses: list) -> str:
    return responses[random.randint(0, len(responses) - 1)]


def get_random_in_range(start: int, end: int):
    return random.randint(start, end)


def get_all_files_in_path(path: str):
    return [f for f in listdir(path) if isfile(join(path, f))]


def remove_doubles_from_list(my_list: list):
    return list(dict.fromkeys(my_list))


def is_permitted(permission_granted: PermissionLevels, permission_required: PermissionLevels):
    if permission_granted == PermissionLevels.ADMINISTRATOR:
        return True
    elif permission_granted == PermissionLevels.MODERATOR:
        return permission_required == PermissionLevels.EVERYBODY or permission_required.MODERATOR
    elif permission_required == PermissionLevels.EVERYBODY:
        return True
    else:
        return False
