import json

from utils import logger


def loadJSON(file: str) -> dict:
    with open(file) as f:
        logger.log(logger.INFO, "Loading JSON: " + file)
        d = json.load(f)
        f.close()
    return d


def save_json(file: str, data):
    with open(file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
