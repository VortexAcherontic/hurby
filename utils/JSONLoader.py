import json

from utils import Logger


def loadJSON(file):
    with open(file) as f:
        Logger.log(Logger.INFO, "Load JSON: " + file)
        d = json.load(f)
        f.close()
    return d