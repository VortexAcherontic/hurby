import json


def loadJSON(file):
    with open(file) as f:
        print("Load JSON: " + file)
        d = json.load(f)
        f.close()
    return d