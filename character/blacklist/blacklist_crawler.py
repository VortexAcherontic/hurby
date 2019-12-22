import os

import requests

from utils import const, json_loader

_TMP_FILE = "external-ban-list.json"
_TMP_FILE_ABSOLUTE = const.CONST.DIR_TMP_ABSOLUTE + "/" + _TMP_FILE


def get_twitch_bot_names() -> dict:
    if _tmp_file_exist():
        return _load_tmp_file()
    else:
        url = "https://raw.githubusercontent.com/tarumes/twitch-ban-list/master/public_ban.json"
        external_json = requests.get(url).json()
        bots = {
            "names": [],
            "ids": []
        }
        for user in external_json:
            if user["reason"] == "bot_account":
                bots["names"].append(user["twitch_name"])
                bots["ids"].append(user["twitch_id"])
        save_tmp_file(bots)
        return bots


def _tmp_file_exist():
    try:
        f = open(_TMP_FILE_ABSOLUTE)
        return True
    except IOError:
        return False


def save_tmp_file(bots: dict):
    json_loader.save_json(_TMP_FILE_ABSOLUTE, bots)


def _load_tmp_file() -> dict:
    return json_loader.load_json(_TMP_FILE_ABSOLUTE)


def delete_tmp_file():
    os.remove(_TMP_FILE_ABSOLUTE)
