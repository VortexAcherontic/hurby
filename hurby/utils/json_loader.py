import json
import os
import shutil

from hurby.utils import logger


def load_json(file: str) -> dict:
    try:
        with open(file) as f:
            logger.log(logger.JSON, "Loading JSON: " + file)
            d = json.load(f)
            f.close()
        return d
    except json.decoder.JSONDecodeError as e:
        if _restore_backup(file):
            return load_json(file)
        logger.log(logger.ERR, "Could not decode json file: " + file)


def save_json(file: str, data):
    _create_backup(file)
    with open(file, 'w+', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
    _remove_backup(file)


def _remove_backup(file: str):
    if os.path.isfile(file + ".bak"):
        os.remove(file + ".bak")


def _restore_backup(file: str):
    if os.path.isfile(file + ".bak"):
        shutil.move(file + ".bak", file)
        return True
    return False


def _create_backup(file: str):
    if os.path.isfile(file):
        shutil.copyfile(file, file + ".bak")
