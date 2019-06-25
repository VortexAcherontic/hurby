import json
from utils import logger


def loadJSON(file: str):
    with open(file) as f:
        logger.log(logger.INFO, "Loading JSON: " + file)
        d = json.load(f)
        f.close()
    return d
