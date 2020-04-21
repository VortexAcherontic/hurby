import json

from utils import logger


def load_json(file: str) -> dict:
    try:
        with open(file) as f:
            logger.log(logger.JSON, "Loading JSON: " + file)
            d = json.load(f)
            f.close()
        return d
    except json.decoder.JSONDecodeError as e:
        logger.log(logger.ERR, "Could not decode json file: "+file)


def save_json(file: str, data):
    with open(file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
